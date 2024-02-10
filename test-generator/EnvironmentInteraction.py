from io import BytesIO
import tarfile
import time
import docker


def get_container():
    # Access Docker container
    client = docker.from_env()
    try:
        container_id = "juliet-top-25-java-code-1"  # todo: currently hardcoded, it'd be better to have it a little more dynamic
        container = client.containers.get(container_id)
    except docker.errors.NotFound:
        raise Exception(f"Container with ID '{container_id}' not found.")
    return container


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
        container.put_archive(
            path=dest_path,
            data=tarstream
        )
        print(f"Successfully copied test to '{dest_path}'.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def run_test_in_docker(container, filename):
    try:
        command = f"./gradlew test --tests testcases.{filename}.* --info"
        exec_id = container.exec_run(command)
        output = exec_id.output.decode('utf-8').strip()
        print(output)
        return output
    except Exception as e:
        print(f"An error occurred while running command '{command}': {str(e)}")


def interact_with_env(test, test_name):
    # Get container reference
    container = get_container()
    # Copy the file to Docker
    copy_test_to_docker(container, test, test_name)
    # Run the code in Docker and return the result:
    #   Do this only at your own risk, just running unknown code in Docker is still not 100% safe, but it's a lot safer than running it on your local machine.
    result = run_test_in_docker(container, test_name)
    return result
