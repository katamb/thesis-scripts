import csv


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
    results = read_csv('spotbugs-result.csv')
    unique_item = []
    for item in results:
        el = item[1].strip()
        if el not in unique_item:
            unique_item.append(el)
    print(unique_item)


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
    aggregate()
