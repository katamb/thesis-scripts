import os
import re


def remove_comments(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Remove multiline comments
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)

    # Remove single-line comments
    content = re.sub(r'// .*', '', content)
    content = re.sub(r' //.*', '', content)

    with open(file_path, 'w') as file:
        file.write(content)


def process_directory(directory_path):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".java"):
                file_path = os.path.join(root, file)
                remove_comments(file_path)


if __name__ == "__main__":
    current_directory = "C:\\Users\\karlt\\thesis\\datasets\\mini-testing\\src\\testcases"  # os.getcwd()
    process_directory(current_directory)
    print("Script completed successfully.")
