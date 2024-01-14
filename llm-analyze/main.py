from dotenv import load_dotenv, find_dotenv
from SimplePromptRunner import SimplePromptRunner
from SelfReflectionPromptRunner import SelfReflectionPromptRunner
import os


def process_directory(directory_path):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if "Main" in file or "Helper" in file:
                continue
            elif file.startswith("J") and file.endswith(".java"):
                file_path = os.path.join(root, file)
                if ("CWE89" in file_path
                        or "CWE78" in file_path
                        or "CWE476" in file_path
                        or "CWE190" in file_path):
                    runner = SelfReflectionPromptRunner(file_path, "dataflow_analysis_prompt")
                    runner.run_prompt()


if __name__ == "__main__":
    load_dotenv(find_dotenv())

    #file = os.environ.get("DATASET_DIRECTORY_ROOT") + "\\src\\testcases\\CWE23_Relative_Path_Traversal\\J1379.java"
    #runner = SelfReflectionPromptRunner(file, "dataflow_analysis_prompt")
    #runner.run_prompt()

    dataset_root = os.environ.get("DATASET_DIRECTORY_ROOT")
    folder = os.path.join(dataset_root, "src", "testcases")
    process_directory(folder)
