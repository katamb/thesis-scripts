from dotenv import load_dotenv, find_dotenv
import os
import re


def count_braces(line):
    count_open = line.count('{')
    count_close = line.count('}')
    return count_open - count_close


def add_text_before_last_dot(input_string, appended_txt):
    if '.' in input_string:
        last_dot_index = input_string.rindex('.')
        modified_string = input_string[:last_dot_index] + '_' + appended_txt + input_string[last_dot_index:]
        return modified_string
    else:
        return input_string + '_' + appended_txt


def get_file_name(file_path):
    last_dot_index = file_path.rindex('.')
    last_slash_index = file_path.rindex('\\') + 1
    file_name = file_path[last_slash_index:last_dot_index]
    return file_name


def split_files(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    good_file = add_text_before_last_dot(file_path, "good")
    bad_file = add_text_before_last_dot(file_path, "bad")
    good_content = ""
    bad_content = ""
    inside_bad_function = False
    inside_good_function = False
    function_braces_count = 0
    for line in content.split("\n"):
        if function_braces_count == 0:
            inside_bad_function = False
            inside_good_function = False

        if line.strip().startswith("public void bad") or line.strip().startswith("private void bad"):
            inside_bad_function = True
            inside_good_function = False
            bad_content += line + "\n"
            function_braces_count += count_braces(line)
        elif line.strip().startswith("public void good") or line.strip().startswith("private void good"):
            inside_good_function = True
            inside_bad_function = False
            good_content += line + "\n"
            function_braces_count += count_braces(line)
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
    good_content = good_content.replace(old_file_name, get_file_name(good_file))
    bad_content = bad_content.replace(old_file_name, get_file_name(bad_file))

    os.rename(file_path, good_file)
    with open(good_file, 'w') as file:
        file.write(good_content)
    with open(bad_file, 'w') as file:
        file.write(bad_content)


def update_file_names(file_path):
    new_content = ""
    with open(file_path, 'r') as file:
        content = file.read()

    for line in content.split("\n"):
        if "_01()" in line:
            new_good_line = line.replace("_01()", "_01_good()")
            new_bad_line = line.replace("_01()", "_01_bad()")
            new_content += new_good_line + "\n"
            new_content += new_bad_line + "\n"
        else:
            new_content += line + "\n"

    with open(file_path, 'w') as file:
        file.write(new_content)

def process_file(file_path):
    lines = []
    with open(file_path, 'r') as file:
        lines = file.readlines()

    with open(file_path, 'w') as file:
        for line in lines:
            if "(new testcases.CWE" not in line or "_01())" in line:
                file.write(line)


def remove_whitespace(file_path):
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
    pattern = r".+_\d+\.java"
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            if file == "Main.java" or file == "ServletMain.java":
                process_file(file_path)
                update_file_names(file_path)
            if "web.xml" == file or "Helper" in file:
                continue
            match = re.match(pattern, file)
            if "CWE" in file and not match:
                os.remove(file_path)
            if "CWE" in file and match:
                remove_comments(file_path)
                remove_whitespace(file_path)
                split_files(file_path)


if __name__ == "__main__":
    load_dotenv(find_dotenv())
    current_dir = os.environ.get("DATASET_DIRECTORY_ROOT") + "\\src\\testcases\\"
    process_directory(current_dir)
