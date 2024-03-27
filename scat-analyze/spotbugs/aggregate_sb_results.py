from dotenv import find_dotenv, load_dotenv
from datetime import date
import csv
import os
import re


file_name_pattern = r"J(\d{5})\.java"
multi_line_match = r"\[lines (\d+)-(\d+)\]"
single_line_match = r"\[line (\d+)\]"
mappings = {
    "D": "Dodgy code (STYLE)",
    "B": "Bad practice (BAD_PRACTICE)",
    "S": "Security (SECURITY)",
    "M": "Multithreaded correctness (MT_CORRECTNESS)",
    "V": "Malicious code vulnerability (MALICIOUS_CODE)",
    "C": "Correctness (CORRECTNESS)",
    "I": "Internationalization (I18N)",
    "X": "Experimental (EXPERIMENTAL)",
    "P": "Performance (PERFORMANCE)"
}


# Reading CSV file
def read_csv(file_path):
    data = []
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            data.append(row)
    return data


# Writing to CSV file
def write_csv(file_path, data):
    with open(file_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=';')
        for row in data:
            csv_writer.writerow(row)


def get_file_name(line):
    match = re.search(file_name_pattern, line)
    if match:
        return f"J{match.group(1)}"
    else:
        raise RuntimeError("Rui")


def does_item_exist(file_name, simplified_results):
    for item in simplified_results:
        if item[0] == file_name:
            return True
    return False


def extract_lines(line):
    match = re.search(multi_line_match, line)
    if match:
        return match.group(1), match.group(2)
    match = re.search(single_line_match, line)
    if match:
        res = match.group(1)
        return res, res
    return "", ""


def aggregate():
    sb_results = read_csv('spotbugs-initial-results.csv')
    simplified_results = []
    for sb_result in sb_results:
        row = [os.environ.get("CURRENT_DATASET_NAME"), "spotbugs"]

        # Get Java file name
        file_name = get_file_name(sb_result[2])  # potentially auto-ignore some Main files etc
        row.append(file_name)

        # Add CWE list
        explanation = sb_result[2]
        row.append("")
        clarification = mappings[sb_result[1].strip()]
        row.append(clarification + " - " + explanation)

        # Add rows
        line_nrs = extract_lines(sb_result[2])
        row.append(line_nrs[0])
        row.append(line_nrs[1])

        # Add date
        row.append(str(date.today()))

        simplified_results.append(row)

    write_csv('spotbugs-results.csv', simplified_results)


if __name__ == "__main__":
    """
    1st col is severity: 
     * H - high
     * M - medium
    2nd col is class:
     * D - Dodgy code (STYLE)
     * B - Bad practice (BAD_PRACTICE)
     * S - Security (SECURITY)
     * M - Multithreaded correctness (MT_CORRECTNESS)
     * V - Malicious code vulnerability (MALICIOUS_CODE)
     * C - Correctness (CORRECTNESS)
     * I - Internationalization (I18N)
     * X - Experimental (EXPERIMENTAL)
     * P - Performance (PERFORMANCE)
    """
    load_dotenv(find_dotenv())
    aggregate()
