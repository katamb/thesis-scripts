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
                runner = SimplePromptRunner(file_path, "modified_noever_prompt")
                runner.run_prompt()


if __name__ == "__main__":
    #file = "C:\\Users\\karlt\\thesis\\datasets\\mini-testing\\src\\testcases\\CWE80_XSS\\s01\\J2628.java"
    #runner = SimplePromptRunner(file, "modified_noever_prompt")
    #runner.run_prompt()
    folder = "C:\\Users\\karlt\\thesis\\datasets\\mini-testing\\src\\testcases\\CWE338_Weak_PRNG"
    process_directory(folder)
