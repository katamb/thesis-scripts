import os


def get_file_name(file_path):
    last_dot_index = file_path.rindex('.')
    last_slash_index = file_path.rindex('\\') + 1
    file_name = file_path[last_slash_index:last_dot_index]
    return file_name


def remove_clues(file_path, counter):
    with open(file_path, 'r') as file:
        content = file.read()

    # Rename functions
    content = content.replace("good()", "process()")
    content = content.replace("good1()", "process1()")
    content = content.replace("good(HttpServletRequest", "process(HttpServletRequest")
    content = content.replace("good1(HttpServletRequest", "process1(HttpServletRequest")
    content = content.replace("good1(request", "process1(request")
    content = content.replace("goodG2B()", "processG2B()")
    content = content.replace("goodG2B(request", "processG2B(request")
    content = content.replace("goodG2B(HttpServletRequest", "processG2B(HttpServletRequest")
    content = content.replace("goodB2G()", "processB2G()")
    content = content.replace("goodB2G(request", "processB2G(request")
    content = content.replace("goodB2G(HttpServletRequest", "processB2G(HttpServletRequest")
    content = content.replace("bad()", "handle()")
    content = content.replace("bad(HttpServletRequest", "handle(HttpServletRequest")

    # Rename file
    old_file_name = get_file_name(file_path)
    new_file_name = "J" + str(counter)
    new_file_path = file_path.replace(old_file_name, new_file_name)
    content = content.replace(old_file_name, new_file_name)
    os.rename(file_path, new_file_path)

    with open(new_file_path, 'w') as file:
        file.write(content)

    with open("C:\\Users\\karlt\\thesis\\datasets\\mini-testing\\file-mapping.csv", "a") as f:
        cwe = old_file_name.split("_")[0]
        cwe_present = "bad" in old_file_name
        cwe_description = " ".join(old_file_name.split("__")[0].split("_")[1:])
        f.write(f"{new_file_name}, {old_file_name}, {cwe}, {cwe_present}, {cwe_description} \n")

    return old_file_name, new_file_name


def process_main_file(file_path, renamings):
    with open(file_path, 'r') as file:
        content = file.read()

    for k in renamings:
        content = content.replace(k + "()", renamings[k] + "()")

    with open(file_path, 'w') as file:
        file.write(content)


def process_directory(directory_path):
    counter = 1000
    for root, dirs, files in os.walk(directory_path):
        renamings = {}
        for file in files:
            if "Helper" in file:
                continue
            elif file.endswith(".java") and "Main" not in file:
                file_path = os.path.join(root, file)
                file_names_tuple = remove_clues(file_path, counter)
                renamings[file_names_tuple[0]] = file_names_tuple[1]
                counter += 1
            elif "Main" in file:
                file_path = os.path.join(root, file)
                process_main_file(file_path, renamings)


if __name__ == "__main__":
    current_directory = "C:\\Users\\karlt\\thesis\\datasets\\mini-testing\\src\\testcases"
    process_directory(current_directory)
    print("Script completed successfully.")
