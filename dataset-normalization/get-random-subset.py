from dotenv import load_dotenv, find_dotenv
import os
import csv
import random
import re


pattern = r'\.J(\d{5})\(\)\)\.runTest\('


def get_matching_el_id(el):
    if "good" in el:
        return el.replace("good", "bad")
    else:
        return el.replace("bad", "good")


def choose_files(mapping_file, amount_of_files_to_keep_per_cwe):
    # Read in the file
    with open(mapping_file, 'r', newline="") as infile:
        reader = csv.reader(infile)
        data = list(reader)

    # Create a dictionary with key as cwe-id and value as list of rows in existing file
    data_map = dict()
    for item in data:
        if "J" not in item[1]:  # Skip header row
            continue
        cwe_id = item[3]
        if cwe_id not in data_map:
            data_map[cwe_id] = [item]
        else:
            curr_list = data_map[cwe_id]
            curr_list.append(item)
            data_map[cwe_id] = curr_list

    new_data = [data[1]]
    for k in data_map:
        current_cwe_list = data_map[k]
        if len(current_cwe_list) > amount_of_files_to_keep_per_cwe:
            reduced_cwe_list = []
            files = []
            count = 0
            while count < amount_of_files_to_keep_per_cwe:
                el_to_pick_index = random.randrange(len(current_cwe_list))
                file_name = current_cwe_list[el_to_pick_index][1]
                if file_name in files:
                    continue
                files.append(file_name)
                matching_el_id = get_matching_el_id(current_cwe_list[el_to_pick_index][2])
                matching_el_row = [sublist for sublist in current_cwe_list if sublist[2] == matching_el_id]
                files.append(matching_el_row[0][1])
                reduced_cwe_list.append(current_cwe_list[el_to_pick_index])
                reduced_cwe_list.append(matching_el_row[0])
                count += 2
            new_data.extend(reduced_cwe_list)
        else:
            new_data.extend(current_cwe_list)

    # Write the modified content to a new CSV file
    with open(mapping_file, 'w', newline="") as outfile:
        writer = csv.writer(outfile)
        sorted_list = sorted(new_data, key=lambda x: x[1])
        for row in sorted_list:
            writer.writerow(row)


def remove_refs_to_removed_files(file_path, mapping_file):
    with open(mapping_file, 'r', newline="") as infile:
        reader = csv.reader(infile)
        mappings = list(reader)
    existing_files = []
    for mapping in mappings:
        existing_files.append(mapping[1])

    with open(file_path, "r") as f:
        content = f.readlines()

    new_content = []
    for line in content:
        match = re.search(pattern, line)
        if match:
            matched_numbers = f"J{match.group(1)}"
            if matched_numbers not in existing_files:
                continue
        new_content.append(line)


    with open(file_path, "w") as f:
        for line in new_content:
            f.write(line)


def remove_files_not_present_in_mapping_file(ds_directory, mapping_file):
    with open(mapping_file, "r") as f:
        content = f.read()

    for root, dirs, files in os.walk(ds_directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file.startswith("J") and file.endswith(".java"):
                if file.split(".")[0] not in content:
                    os.remove(file_path)
            elif "Main" in file:
                remove_refs_to_removed_files(file_path, mapping_file)


if __name__ == "__main__":
    load_dotenv(find_dotenv())
    amount_of_files_to_keep_per_cwe = 34  # Has to be positive even integer
    mapping_file = os.environ.get("DATASET_DIRECTORY_ROOT") + "\\file-mapping.csv"
    choose_files(mapping_file, amount_of_files_to_keep_per_cwe)
    ds_directory = os.environ.get("DATASET_DIRECTORY_ROOT") + "\\src\\testcases\\"
    remove_files_not_present_in_mapping_file(ds_directory, mapping_file)
    print("Script completed successfully.")
