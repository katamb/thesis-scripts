import os


def process_file(file_path):
    lines = []
    with open(file_path, 'r') as file:
        lines = file.readlines()

    with open(file_path, 'w') as file:
        for line in lines:
            if "(new testcases.CWE" not in line or "_01())" in line:
                file.write(line)


def process_directory(directory_path):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file == "Main.java" or file == "ServletMain.java":
                file_path = os.path.join(root, file)
                print(file_path)
                process_file(file_path)


"""
Run through all files in subdirectories and remove references to the unused lines
"""
if __name__ == "__main__":
    current_directory = "C:\\Users\\karlt\\thesis\\datasets\\mini-testing\\src\\testcases"  # os.getcwd()
    process_directory(current_directory)
    print("Script completed successfully.")