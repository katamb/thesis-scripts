import os


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


def process_directory(directory_path):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if "good" in file or "bad" in file:
                continue
            file_path = os.path.join(root, file)
            if "CWE" in file and file.endswith(".java"):
                split_files(file_path)
            elif "Main" in file:
                update_file_names(file_path)


if __name__ == "__main__":
    current_directory = "C:\\Users\\karlt\\thesis\\datasets\\mini-testing\\src\\testcases"  # os.getcwd()
    process_directory(current_directory)
    print("Script completed successfully.")
