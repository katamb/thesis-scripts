from dotenv import load_dotenv, find_dotenv
#from SimplePromptRunner import SimplePromptRunner
#from ReActRunner import ReActRunner
#from SelfReflectionPromptRunner import SelfReflectionPromptRunner
from CriticiseRefinePromptRunner import CriticiseRefinePromptRunner
from concurrent.futures import ThreadPoolExecutor
import os
import threading


def run_prompt(file_path, lock=threading.Lock()):
    runner = CriticiseRefinePromptRunner(file_path,
                                         "cot_prompt_rci",
                                         [
                                             ("cot_prompt_rci_criticise", "cot_prompt_rci_improve"),
                                             ("cot_prompt_rci_criticise_short", "cot_prompt_rci_improve_short")
                                         ],
                                         lock)
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
                elif file.startswith("J") and file.endswith(".java") and "J11608" not in file:
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
    dataset_root = os.environ.get("DATASET_DIRECTORY_ROOT")

    # C:\Users\karlt\thesis\datasets\juliet-top-25\src\testcases\CWE129_Improper_Validation_of_Array_Index\s03\J11608.java
    #file = os.path.join(dataset_root, "src", "testcases", "CWE129_Improper_Validation_of_Array_Index", "s03", "J11608.java")
    #run_prompt(file)

    folder = os.path.join(dataset_root, "src", "testcases")
    process_directory_concurrently(folder)
