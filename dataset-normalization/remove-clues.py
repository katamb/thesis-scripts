import os
from dotenv import load_dotenv, find_dotenv


"""
Some CWE's have sub-classes of vulnerabilities.
For example, CWE-22 (Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal')) is a parent 
of CWE-23 and CWE-36. If the file claims to contain CWE-22, but some tool identifies it as CWE-23, it should still count
as valid response, as the response is simply more accurate.
"""
acceptable_mappings = {
    "CWE-23": ["CWE-22", "CWE-23", "CWE-24", "CWE-25", "CWE-26", "CWE-27", "CWE-28", "CWE-29", "CWE-30", "CWE-31", "CWE-32", "CWE-33", "CWE-34"],
    "CWE-36": ["CWE-22", "CWE-36", "CWE-37", "CWE-38", "CWE-39", "CWE-40"],
    "CWE-78": ["CWE-78", "CWE-77"],
    "CWE-80": ["CWE-80", "CWE-79"],
    "CWE-81": ["CWE-81", "CWE-79"],
    "CWE-83": ["CWE-83", "CWE-79", "CWE-82"],
    "CWE-89": ["CWE-89", "CWE-564", "CWE-943"],
    "CWE-129": ["CWE-129", "CWE-1285"],
    "CWE-190": ["CWE-190", "CWE-680"],
    "CWE-256": ["CWE-256", "CWE-522"],
    "CWE-259": ["CWE-259", "CWE-798"],
    "CWE-321": ["CWE-321", "CWE-798"],
    "CWE-476": ["CWE-476"],
    "CWE-523": ["CWE-522", "CWE-523"],
    "CWE-549": ["CWE-522", "CWE-549"],
    "CWE-566": ["CWE-566", "CWE-639"],
    "CWE-606": ["CWE-606", "CWE-1284"]
}


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
    content = content.replace("goodG2B1()", "processG2B1()")
    content = content.replace("goodG2B2()", "processG2B2()")
    content = content.replace("goodG2B(request", "processG2B(request")
    content = content.replace("goodG2B(HttpServletRequest", "processG2B(HttpServletRequest")
    content = content.replace("goodB2G()", "processB2G()")
    content = content.replace("goodB2G1()", "processB2G1()")
    content = content.replace("goodB2G2()", "processB2G2()")
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

    root_dir = os.environ.get('DATASET_DIRECTORY_ROOT')
    with open(root_dir + "\\file-mapping.csv", "a") as f:
        cwe = old_file_name.split("_")[0]
        cwe_id = f"CWE-{cwe[3:]}"
        cwe_present = "bad" in old_file_name
        cwe_description = " ".join(old_file_name.split("__")[0].split("_")[1:])
        accepted_cwe_ids = " ".join(acceptable_mappings[cwe_id])
        f.write(f"{new_file_name},{old_file_name},{cwe_id},{cwe_present},{accepted_cwe_ids},{cwe_description}\n")

    return old_file_name, new_file_name


def process_main_file(file_path, renamings):
    with open(file_path, 'r') as file:
        content = file.read()

    for k in renamings:
        content = content.replace(k + "()", renamings[k] + "()")

    with open(file_path, 'w') as file:
        file.write(content)


def process_directory(directory_path):
    counter = 10000
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
    load_dotenv(find_dotenv())
    root_dir = os.environ.get('DATASET_DIRECTORY_ROOT')
    # Create mapping file
    mapping_file = root_dir + "\\file-mapping.csv"
    if not os.path.exists(mapping_file):
        with open(mapping_file, "w") as f:
            f.write("file_name,original_file_name,cwe_id,cwe_present,acceptable_cwe_ids,cwe_description\n")
    # Run clue-removal script
    current_dir = root_dir + "\\src\\testcases\\"
    process_directory(current_dir)
    print("Script completed successfully.")
