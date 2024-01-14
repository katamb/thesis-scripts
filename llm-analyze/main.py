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
                runner = SelfReflectionPromptRunner(file_path, "dataflow_analysis_prompt")
                runner.run_prompt()


if __name__ == "__main__":
    load_dotenv(find_dotenv())
    file = os.environ.get("DATASET_DIRECTORY_ROOT") + "\\src\\testcases\\CWE23_Relative_Path_Traversal\\J1376.java"
    runner = SelfReflectionPromptRunner(file, "dataflow_analysis_prompt")
    runner.run_prompt()
    #folder = "C:\\Users\\karlt\\thesis\\datasets\\mini-testing\\src\\testcases\\CWE338_Weak_PRNG"
    #process_directory(folder)
