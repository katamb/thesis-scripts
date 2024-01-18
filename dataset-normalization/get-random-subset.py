from dotenv import load_dotenv, find_dotenv
import os
import csv
import random


def choose_files(mapping_file, amount_of_files_to_keep_per_cwe):
    with open(mapping_file, 'r', newline="") as infile:
        reader = csv.reader(infile)
        data = list(reader)

    data_map = dict()
    for item in data:
        if "J" not in item[0]:  # Skip header row
            continue
        cwe_id = item[2]
        cwe_present = item[3]
        key = f"{cwe_id}-{cwe_present}"
        if key not in data_map:
            data_map[key] = [item]
        else:
            curr_list = data_map[key]
            curr_list.append(item)
            data_map[key] = curr_list

    amount_of_files_to_keep_per_cwe = amount_of_files_to_keep_per_cwe / 2
    new_data = [data[0]]
    for k in data_map:
        current_cwe_list = data_map[k]
        if len(current_cwe_list) > amount_of_files_to_keep_per_cwe:
            amount_of_items_to_remove = int(len(current_cwe_list) - amount_of_files_to_keep_per_cwe)
            for i in range(amount_of_items_to_remove):
                current_cwe_list.pop(random.randrange(len(current_cwe_list)))
        new_data.extend(current_cwe_list)

    # Write the modified content to a new CSV file

    with open(mapping_file, 'w', newline="") as outfile:
        writer = csv.writer(outfile)
        for row in new_data:
            writer.writerow(row)


def remove_files_not_present_in_mapping_file(ds_directory, mapping_file):
    with open(mapping_file, "r") as f:
        content = f.read()

    for root, dirs, files in os.walk(ds_directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file.startswith("J") and file.endswith(".java"):
                if file.split(".")[0] not in content:
                    os.remove(file_path)


if __name__ == "__main__":
    load_dotenv(find_dotenv())
    amount_of_files_to_keep_per_cwe = 34  # Has to be positive even integer
    mapping_file = os.environ.get("DATASET_DIRECTORY_ROOT") + "\\file-mapping.csv"
    # todo potentially select file-pairs
    choose_files(mapping_file, amount_of_files_to_keep_per_cwe)
    ds_directory = os.environ.get("DATASET_DIRECTORY_ROOT") + "\\src\\testcases\\"
    remove_files_not_present_in_mapping_file(ds_directory, mapping_file)
    print("Script completed successfully.")
