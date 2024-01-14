import os
import re


def get_matching_cwes():
    with open("./categories/juliet-cwes", 'r') as file:
        juliet_cwes = file.readlines()

    with open("./categories/poor-coding-practices", 'r') as file:
        pcp_cwes = file.readlines()

    not_affected_cwes = []
    affected_cwes = []
    for el_j in juliet_cwes:
        if el_j in pcp_cwes:
            affected_cwes.append(el_j.replace("\n", ""))
        else:
            not_affected_cwes.append(el_j.replace("\n", ""))
    not_affected_cwes.sort()
    affected_cwes.sort()
    print(f"affected {affected_cwes}")
    print(f"not affected {not_affected_cwes}")


def get_cwe(file_path):
    match = re.search(r'CWE(\d+)_', file_path)
    if match:
        return match.group(1)
    else:
        return None
    #return filename.split("_")[0]


def process_directory(directory_path):
    count = 0
    count_per_cwe = dict()
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            if file.startswith("J") and file.endswith(".java"):
                count += 1
                cwe = "CWE-" + get_cwe(file_path)
                if cwe in count_per_cwe:
                    currcount = count_per_cwe[cwe]
                    count_per_cwe[cwe] = currcount + 1
                else:
                    print(cwe)
                    count_per_cwe[cwe] = 1
    print("Amount of files " + str(count))
    print(count_per_cwe)


if __name__ == "__main__":
    current_directory = "C:\\Users\\karlt\\thesis\\datasets\\juliet-top-25\\src\\testcases"
    process_directory(current_directory)
    print("Script completed successfully.")
    #get_matching_cwes()