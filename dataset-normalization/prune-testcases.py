from dotenv import load_dotenv, find_dotenv
import os
import re


pattern_to_keep = r".+_\d+\.java"
pattern_to_remove = r".+_\d+a\(\)\)\.runTest"


def process_main_file(file_path):
    with open(file_path, 'r') as file:
        content = file.readlines()

    new_content = []
    for line in content:
        match = re.match(pattern_to_remove, line)
        if not match:
            new_content.append(line)

    with open(file_path, 'w') as file:
        for l in new_content:
            file.write(l)


def process_directory(directory_path):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            match = re.match(pattern_to_keep, file)
            if "Main" in file:
                process_main_file(file_path)
            elif "web.xml" == file or "Helper" in file:
                continue
            elif "CWE" in file and not match:
                os.remove(file_path)


if __name__ == "__main__":
    load_dotenv(find_dotenv())
    current_directory = os.environ.get("DATASET_DIRECTORY_ROOT") + "\\src\\testcases\\"
    process_directory(current_directory)
    print("Script completed successfully.")