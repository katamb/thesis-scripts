import os


def process_directory(directory_path):
    count = 0
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.startswith("J") and file.endswith(".java"):
                count += 1
    print("Amount of files " + str(count))


if __name__ == "__main__":
    current_directory = "C:\\Users\\karlt\\thesis\\datasets\\mini-testing\\src\\testcases"  # os.getcwd()
    process_directory(current_directory)
    print("Script completed successfully.")
