import csv


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
    mappings = read_csv('codeql-mappings.csv')
    results = read_csv('codeql-results.csv')
    simplified_results = []
    for item in results:
        row = []
        if item[0] == "Name":
            continue
        file_name = get_file_name(item[4])
        if not file_name.startswith("J"):
            continue
        explanation = item[0]
        row.append(file_name)
        cwes = ""
        for mapping in mappings:
            if mapping[3] == explanation:
                cwes += mapping[0] + " "
        row.append(cwes.strip())

        item_exists = does_item_exist(file_name, simplified_results)
        if item_exists:
            for obj in simplified_results:
                if obj[0] == file_name and obj[1] != cwes.strip():
                    obj[1] = obj[1] + " " + cwes.strip()
        else:
            simplified_results.append(row)

    write_csv('simplified-results.csv', simplified_results)


def add_to_file_data():
    mappings = read_csv('file-mapping.csv')
    results = read_csv('simplified-results.csv')
    for mapping in mappings:
        if mapping[0] == "new file name":
            continue

        for item in results:
            if item[0] == mapping[0]:
                mapping.append(item[1])

    write_csv('file-mapping.csv', mappings)


def print_supported_cwes():
    mappings = read_csv('codeql-mappings.csv')
    results = []
    for item in mappings:
        el = item[0].strip()
        if el not in results:
            results.append(el)
    print(results)


def print_juliet_cwes():
    mappings = read_csv('file-mapping.csv')
    results = []
    for item in mappings:
        el = item[2].strip()
        if el not in results:
            results.append(el)
            print(el)
    print(results)


if __name__ == "__main__":
    #aggregate()
    #add_to_file_data()
    print_juliet_cwes()
