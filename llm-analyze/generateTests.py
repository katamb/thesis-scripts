from dotenv import load_dotenv, find_dotenv
import os
from TestGenerator import TestGenerator
import docker
import tarfile
import time
import re
from io import BytesIO


file_name_pattern = r"J(\d{5})\.java"


def generate_test(test_generator):
    llm_output = test_generator.run_prompt()
    test_code = llm_output.replace("```java", "").replace("```", "")
    return test_code


def generate_improved_test(test_generator, improvement_prompt):
    llm_output = test_generator.run_additional_prompt(improvement_prompt)
    test_code = llm_output.replace("```java", "").replace("```", "")
    return test_code


def copy_test_to_docker(container, test, test_name):
    # Idea from: https://gist.github.com/zbyte64/6800eae10ce082bb78f0b7a2cca5cbc2
    tarstream = BytesIO()
    tar = tarfile.TarFile(fileobj=tarstream, mode="w")
    file_data = test.encode("utf8")
    tarinfo = tarfile.TarInfo(name=f"{test_name}.java")
    tarinfo.size = len(file_data)
    tarinfo.mtime = time.time()
    tarinfo.mode = 0o755
    tar.addfile(tarinfo, BytesIO(file_data))
    tar.close()
    tarstream.seek(0)
    try:
        dest_path = "/app/src/test/java/testcases"
        pr = container.put_archive(
            path=dest_path,
            data=tarstream
        )
        print(pr)
        print(f"Successfully copied test to '{dest_path}'.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def run_test_in_docker(container, filename):
    try:
        command = f"./gradlew test --tests testcases.{filename}.*"
        exec_id = container.exec_run(command)
        output = exec_id.output.decode('utf-8').strip()
        #print(f"Command '{command}' executed successfully:\n{output}")
        return output
    except Exception as e:
        print(f"An error occurred while running command '{command}': {str(e)}")


def flow_manager(file_path):
    # Access Docker container
    client = docker.from_env()
    try:
        container_id = "juliet-top-25-app-1"  # todo: currently hardcoded, it'd be better to have it a little more dynamic
        container = client.containers.get(container_id)
    except docker.errors.NotFound:
        print(f"Container with ID '{container_id}' not found.")
        return


    match = re.search(file_name_pattern, file_path)
    if match:
        test_name = f"J{match.group(1)}Test"
    else:
        print(f"Failed getting file name from path {file_path}.")
        return

    test_generator = TestGenerator(file_path, "test_gen", "CWE-129", test_name)
    test = generate_test(test_generator)
    copy_test_to_docker(container, test, test_name)
    result = run_test_in_docker(container, test_name)

    if "Compilation failed" in result:
        improvement_needed_prompt = "The tests did not compile. I will give you the output and based on that you will fix the tests. The output must contain only the fixed tests, nothing else. The output: \n" + result
        test = generate_improved_test(test_generator, improvement_needed_prompt)
        copy_test_to_docker(container, test, test_name)
        result = run_test_in_docker(container, test_name)

    return result


if __name__ == "__main__":
    load_dotenv(find_dotenv())
    dataset_root = os.environ.get("DATASET_DIRECTORY_ROOT")

    #file = os.path.join(dataset_root, "src", "testcases", "CWE129_Improper_Validation_of_Array_Index", "s03", "J11608.java")
    file = os.path.join(dataset_root, "src", "testcases", "CWE129_Improper_Validation_of_Array_Index", "s01", "J10677.java")
    print(flow_manager(file))
