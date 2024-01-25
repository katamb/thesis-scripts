from dotenv import load_dotenv, find_dotenv
from SimplePromptRunner import SimplePromptRunner
from SelfReflectionPromptRunner import SelfReflectionPromptRunner
from concurrent.futures import ThreadPoolExecutor
import os


def run_prompt(file_path):
    runner = SelfReflectionPromptRunner(file_path, "dataflow_analysis_prompt")
    runner.run_prompt()


def process_directory(directory_path):
    counter = 0
    for root, dirs, files in os.walk(directory_path):
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            for file in files:
                if "Main" in file or "Helper" in file:
                    continue
                elif file.startswith("J") and file.endswith(".java"):
                    file_path = os.path.join(root, file)
                    if ("CWE89" in file_path
                            or "CWE78" in file_path
                            #or "CWE476" in file_path
                            #or "CWE190" in file_path
                    ):
                        counter += 1
                        print(counter)
                        future = executor.submit(run_prompt, file_path)
                        futures.append(future)

            # Wait for all tasks to complete
            for future in futures:
                future.result()


if __name__ == "__main__":
    load_dotenv(find_dotenv())

    file = os.environ.get("DATASET_DIRECTORY_ROOT") + "\\src\\testcases\\CWE23_Relative_Path_Traversal\\J18272.java"
    runner = SelfReflectionPromptRunner(file, "dataflow_analysis_prompt")
    runner.run_prompt()

    #dataset_root = os.environ.get("DATASET_DIRECTORY_ROOT")
    #folder = os.path.join(dataset_root, "src", "testcases")
    #process_directory(folder)
