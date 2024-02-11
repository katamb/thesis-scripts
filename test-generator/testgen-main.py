from dotenv import load_dotenv, find_dotenv
from TestGeneratorModel import TestGeneratorModel
from EvaluatorModel import EvaluatorModel
from EnvironmentInteraction import interact_with_env
import re
import os


def get_file_and_test_name(file_path: str) -> str:
    file_name_pattern = r"J(\d{5})\.java"
    match = re.search(file_name_pattern, file_path)
    file_nr = match.group(1)
    if match:
        test_name = f"J{file_nr}", f"J{file_nr}Test"
        return test_name
    else:
        raise Exception(f"Failed getting file name from path {file_path}.")


def load_file_content(file_path: str) -> str:
    with open(file_path, 'r') as file:
        content = file.readlines()

    for i, line in enumerate(content):  # remove whitespace to save on tokens
        content[i] = line.strip()
    return "\n".join(content)


def save_result_row(file_name: str, is_true_positive: bool):
    with open("results.csv", "a") as res:
        res.write(
            f"{file_name};"
            f"{is_true_positive}\n"
        )


def get_cwe_from_path(file_path: str) -> str:
    match = re.search(r'CWE(\d+)_', file_path)
    if match:
        return f"CWE-{match.group(1)}"
    else:
        raise Exception("Unable to get the CWE")


def main(file_path: str):
    # Get the name for the test to be generated
    file_and_test_name = get_file_and_test_name(file_path)
    file_name = file_and_test_name[0]
    test_name = file_and_test_name[1]
    cwe_id = get_cwe_from_path(file_path)
    code = load_file_content(file_path)
    test_generator_model = TestGeneratorModel(file_path)
    evaluation_model = EvaluatorModel(file_path)

    # Initial evaluation of whether the file can be tested
    evaluation_result = evaluation_model.run_prompt(
        "initial_evaluate", {"code": code, "cwe-id": cwe_id}
    )
    if "Can't be unit tested" in evaluation_result:
        save_result_row(file_name, True)
        print("File: ", file_path, " can't be unit tested, considering result as TP.")
        return

    # Generate initial tests
    test_gen_result = test_generator_model.run_prompt(
        "initial_test_gen", {"code": code, "cwe-id": cwe_id, "test-name": test_name, "evaluation-result": evaluation_result}
    )
    test_running_result = interact_with_env(test_gen_result, test_name)
    # Fix compilation errors
    if "Compilation failed" in test_running_result:
        test_gen_result = test_generator_model.run_prompt(
            "test_gen_reflection", {"test-run-result": test_running_result}
        )
        test_running_result = interact_with_env(test_gen_result, test_name)

    # Evaluate testing results
    evaluation_result = evaluation_model.run_prompt(
        "evaluate", {"test-code": test_gen_result, "test-result": test_running_result}
    )
    if "The analysis results are false positive" in evaluation_result:
        save_result_row(file_name, False)
        print("File: ", file_path, " is considered false positive.")
        return
    if "The analysis results are true positive" in evaluation_result:
        save_result_row(file_name, True)
        print("File: ", file_path, " is considered true positive.")
        return

    # FUTURE loop start
    # Regen tests
    test_gen_result = test_generator_model.run_prompt(
        "test_gen", {"feedback": evaluation_result}
    )
    test_running_result = interact_with_env(test_gen_result, test_name)
    evaluation_result = evaluation_model.run_prompt(
        "evaluate", {"test-code": test_gen_result, "test-result": test_running_result}
    )
    if "The analysis results are false positive" in evaluation_result:
        save_result_row(file_name, False)
        print("File: ", file_path, " is considered false positive.")
        return
    if "The analysis results are true positive" in evaluation_result:
        save_result_row(file_name, True)
        print("File: ", file_path, " is considered true positive.")
        return
    # FUTURE loop end

    return test_running_result


if __name__ == "__main__":
    load_dotenv(find_dotenv())
    dataset_root = os.environ.get("DATASET_DIRECTORY_ROOT")

    file = os.path.join(dataset_root, "src", "testcases", "CWE129_Improper_Validation_of_Array_Index", "s03", "J11608.java")
    #file = os.path.join(dataset_root, "src", "testcases", "CWE129_Improper_Validation_of_Array_Index", "s01", "J10677.java")
    print(main(file))
