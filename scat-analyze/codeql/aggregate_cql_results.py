from dotenv import find_dotenv, load_dotenv
from datetime import date
import csv
import os


# Reading CSV file
def read_csv(file_path):
    data = []
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            data.append(row)
    return data


# Writing to CSV file
def write_csv(file_path, data):
    with open(file_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        for row in data:
            csv_writer.writerow(row)


def get_file_name(path):
    last_slash_index = path.rindex('/') + 1
    last_dot_index = path.rindex('.')
    file_name = path[last_slash_index:last_dot_index]
    return file_name


def does_item_exist(file_name, simplified_results):
    for item in simplified_results:
        if item[0] == file_name:
            return True
    return False


def aggregate():
    cql_mappings = read_csv('codeql-mappings.csv')
    cql_results = read_csv('codeql-initial-results.csv')
    simplified_results = []
    for cql_result in cql_results:
        row = [os.environ.get("CURRENT_DATASET_NAME"), "codeql"]

        # Get Java file name
        file_name = get_file_name(cql_result[4])
        if not file_name.startswith("J"):  # Only look at files starting with "J"
            continue
        row.append(file_name)

        # Add CWE list
        explanation = cql_result[0]
        cwes = ""
        for mapping in cql_mappings:
            if mapping[3] == explanation:
                cwes += mapping[0] + " "
        row.append(cwes.strip())
        row.append(explanation)

        # Add rows
        row.append(cql_result[5])
        row.append(cql_result[7])

        # Add date
        row.append(str(date.today()))

        simplified_results.append(row)

    write_csv('codeql-results.csv', simplified_results)


if __name__ == "__main__":
    load_dotenv(find_dotenv())
    aggregate()
