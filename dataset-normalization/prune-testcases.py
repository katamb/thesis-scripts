from dotenv import load_dotenv, find_dotenv
import os
import re


# Keep all files that have a number at the end, specific to the Juliet Java 1.3 dataset
pattern_to_keep = r".+_\d+\.java"
# Remove from main files the references to the removed files
pattern_to_remove = r".+_\d+a\(\)\)\.runTest"


def process_main_file(file_path):
    # Open the Main java file (this is the file that calls code in the test files, the Main files themselves are not for testing)
    with open(file_path, "r") as file:
        content = file.readlines()

    new_content = []
    for line in content:
        match = re.match(pattern_to_remove, line)
        # Skip the lines that match
        if not match:
            new_content.append(line)

    # Write the file
    with open(file_path, "w") as file:
        for line in new_content:
            file.write(line)


def process_directory(directory_path):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            match = re.match(pattern_to_keep, file)
            # Main files need to be processed
            if "Main" in file:
                process_main_file(file_path)
            # xml and Helper files can be left as-is
            elif "web.xml" == file or "Helper" in file:
                continue
            # The matching CWE files need to be removed
            elif "CWE" in file and not match:
                os.remove(file_path)


if __name__ == "__main__":
    load_dotenv(find_dotenv())
    current_directory = os.path.join(os.environ.get("DATASET_DIRECTORY_ROOT"), "src", "testcases")
    process_directory(current_directory)
    print("Script completed successfully.")
