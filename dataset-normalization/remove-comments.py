from dotenv import load_dotenv, find_dotenv
import os
import re


def remove_extra_whitespace(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Split the text into lines
    lines = content.split('\n')

    # Remove trailing whitespace from each line
    lines = [line.rstrip() for line in lines]

    # Remove empty lines
    non_empty_lines = [line for line in lines if line]

    # Join the non-empty lines back into a single string
    cleaned_text = '\n'.join(non_empty_lines)

    with open(file_path, 'w') as file:
        file.write(cleaned_text)


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
            if file.startswith("CWE") and file.endswith(".java"):
                file_path = os.path.join(root, file)
                remove_comments(file_path)
                remove_extra_whitespace(file_path)


if __name__ == "__main__":
    load_dotenv(find_dotenv())
    current_directory = os.environ.get("DATASET_DIRECTORY_ROOT") + "\\src\\testcases\\"
    process_directory(current_directory)
    print("Script completed successfully.")
