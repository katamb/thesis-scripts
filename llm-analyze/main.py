from SimplePromptRunner import SimplePromptRunner
import os


def process_directory(directory_path):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if "Main" in file or "Helper" in file:
                continue
            elif file.startswith("J") and file.endswith(".java"):
                file_path = os.path.join(root, file)
                print(file_path)


if __name__ == "__main__":
    file = "C:\\Users\\karlt\\thesis\\datasets\\mini-testing\\src\\testcases\\CWE23_Relative_Path_Traversal\\J1774.java"
    runner = SimplePromptRunner(file)
    runner.run_prompt()
