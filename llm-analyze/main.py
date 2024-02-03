from dotenv import load_dotenv, find_dotenv
# from SimplePromptRunner import SimplePromptRunner
from ReActRunner import ReActRunner
from SelfReflectionPromptRunner import SelfReflectionPromptRunner
from CriticiseRefinePromptRunner import CriticiseRefinePromptRunner
from concurrent.futures import ThreadPoolExecutor
import os


def run_prompt(file_path):
    runner = CriticiseRefinePromptRunner(file_path, "basic_prompt_rci", "basic_prompt_rci_criticise", "basic_prompt_rci_improve")
    runner.run_prompt()


def process_directory_concurrently(directory_path):
    counter = 0
    for root, dirs, files in os.walk(directory_path):
        with ThreadPoolExecutor(max_workers=14) as executor:
            futures = []
            for file in files:
                if "Main" in file or "Helper" in file:
                    continue
                elif file.startswith("J") and file.endswith(".java"):
                    file_path = os.path.join(root, file)
                    counter += 1
                    print("x-count", counter)
                    future = executor.submit(run_prompt, file_path)
                    futures.append(future)

            # Wait for all tasks to complete
            for future in futures:
                future.result()


def process_directory(directory_path):
    for root, dirs, files in os.walk(directory_path):
            for file in files:
                if "Main" in file or "Helper" in file:
                    continue
                elif file.startswith("J") and file.endswith(".java"):
                    file_path = os.path.join(root, file)
                    run_prompt(file_path)


if __name__ == "__main__":
    load_dotenv(find_dotenv())

    #file = os.environ.get("DATASET_DIRECTORY_ROOT") + "\\src\\testcases\\CWE190_Integer_Overflow\\s02\\J14351.java"
    #runner = CriticiseRefinePromptRunner(file, "basic_prompt_rci", "basic_prompt_rci_criticise", "basic_prompt_rci_improve")
    #runner.run_prompt()

    dataset_root = os.environ.get("DATASET_DIRECTORY_ROOT")
    folder = os.path.join(dataset_root, "src", "testcases")
    process_directory_concurrently(folder)
