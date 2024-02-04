from dotenv import load_dotenv, find_dotenv
from SimplePromptRunner import SimplePromptRunner
from ReActRunner import ReActRunner
from SelfReflectionPromptRunner import SelfReflectionPromptRunner
from CriticiseRefinePromptRunner import CriticiseRefinePromptRunner
from concurrent.futures import ThreadPoolExecutor
import os
import threading


def run_prompt(file_path, lock=threading.Lock()):
    runner = SelfReflectionPromptRunner(file_path, "basic_prompt_sr", lock)
    runner.run_prompt()


def process_directory_concurrently(directory_path):
    lock = threading.Lock()
    counter = 0
    for root, dirs, files in os.walk(directory_path):
        with ThreadPoolExecutor(max_workers=17) as executor:
            futures = []
            for file in files:
                if "Main" in file or "Helper" in file:
                    continue
                elif file.startswith("J") and file.endswith(".java"):
                    file_path = os.path.join(root, file)
                    counter += 1
                    print("x-count", counter)
                    future = executor.submit(run_prompt, file_path, lock)
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

    # C:\Users\karlt\thesis\datasets\juliet-top-25\src\testcases\CWE566_Authorization_Bypass_Through_SQL_Primary\J19871.java
    #file = os.environ.get("DATASET_DIRECTORY_ROOT") + "\\src\\testcases\\CWE78_OS_Command_Injection\\J20841.java"
    #runner = CriticiseRefinePromptRunner(file, "basic_prompt_rci", "basic_prompt_rci_criticise", "basic_prompt_rci_improve")
    #runner.run_prompt()

    dataset_root = os.environ.get("DATASET_DIRECTORY_ROOT")
    folder = os.path.join(dataset_root, "src", "testcases")
    process_directory_concurrently(folder)
