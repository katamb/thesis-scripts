from dotenv import load_dotenv, find_dotenv
import os
import re


# The pattern matches function calls in Main files
pattern = r"__([^)]+)\(\)\)\.runTest"


def count_braces(line):
    count_open = line.count("{")
    count_close = line.count("}")
    return count_open - count_close


def add_text_before_last_dot(input_string, appended_txt):
    # Add the appendix before the last dot (before the file extension)
    if "." in input_string:
        last_dot_index = input_string.rindex(".")
        modified_string = input_string[:last_dot_index] + "_" + appended_txt + input_string[last_dot_index:]
        return modified_string
    else:
        return input_string + "_" + appended_txt


def get_file_name(file_path):
    # Return the file name without extension and path
    last_dot_index = file_path.rindex(".")
    last_slash_index = file_path.rindex(os.sep) + 1
    file_name = file_path[last_slash_index:last_dot_index]
    return file_name


def split_files(file_path):
    # Open the testcase file
    with open(file_path, "r") as file:
        content = file.read()

    good_file_name = add_text_before_last_dot(file_path, "good")
    bad_file_name = add_text_before_last_dot(file_path, "bad")
    good_content = ""
    bad_content = ""
    inside_bad_function = False
    inside_good_function = False
    skip_count_check = False
    function_braces_count = 0

    # Go through the test-case file line-by-line
    for line in content.split("\n"):
        if function_braces_count == 0 and not skip_count_check:
            inside_bad_function = False
            inside_good_function = False
        skip_count_check = False

        # Detect the beginning of a bad function
        if line.strip().startswith("public void bad") or line.strip().startswith("private void bad"):
            inside_bad_function = True
            inside_good_function = False
            bad_content += line + "\n"
            if "{" in line and "}" not in line:
                skip_count_check = True
            function_braces_count += count_braces(line)
        # Detect the beginning of a good function
        elif line.strip().startswith("public void good") or line.strip().startswith("private void good"):
            inside_good_function = True
            inside_bad_function = False
            good_content += line + "\n"
            if "{" in line and "}" not in line:
                skip_count_check = True
            function_braces_count += count_braces(line)
        # Separate the bad and good functions
        elif inside_bad_function:
            bad_content += line + "\n"
            function_braces_count += count_braces(line)
        elif inside_good_function:
            good_content += line + "\n"
            function_braces_count += count_braces(line)
        else:
            bad_content += line + "\n"
            good_content += line + "\n"

    old_file_name = get_file_name(file_path)
    good_content = good_content.replace(old_file_name, get_file_name(good_file_name))
    bad_content = bad_content.replace(old_file_name, get_file_name(bad_file_name))

    # Rename the existing file to the "good" file
    os.rename(file_path, good_file_name)
    with open(good_file_name, "w") as file:
        # Overwrite the existing file that was renamed to the "good" file with the file contents
        file.write(good_content)
    with open(bad_file_name, "w") as file:
        # Write a new file with the "bad" content
        file.write(bad_content)


def update_file_names(file_path):
    new_content = ""
    # Open the Main file
    with open(file_path, "r") as file:
        content = file.read()

    for line in content.split("\n"):
        match = re.search(pattern, line)
        # If match, then duplicate the line, adding "_good" in the end of one function call and "_bad" at the end of the other
        if match:
            extracted_text = match.group(1)
            new_good_line = line.replace(extracted_text, extracted_text + "_good")
            new_bad_line = line.replace(extracted_text, extracted_text + "_bad")
            new_content += new_good_line + "\n"
            new_content += new_bad_line + "\n"
        # If no match, just add regular line
        else:
            new_content += line + "\n"

    # Write the Main file
    with open(file_path, "w") as file:
        file.write(new_content)


def process_directory(directory_path):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            # skip already converted files
            if "good" in file or "bad" in file or "Helper" in file:
                continue
            elif "Main" in file:
                # Change file names in main files that call the files
                update_file_names(file_path)
            elif "CWE" in file and file.endswith(".java"):
                # Split files matching that into 2: good and bad case
                split_files(file_path)


if __name__ == "__main__":
    load_dotenv(find_dotenv())
    current_directory = os.path.join(os.environ.get("DATASET_DIRECTORY_ROOT"), "src", "testcases")
    process_directory(current_directory)
    print("Script completed successfully.")
