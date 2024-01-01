import os


def clean_text(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Split the text into lines
    lines = content.split('\n')

    # Remove trailing whitespace from each line
    lines = [line.rstrip() for line in lines]

    # Remove empty lines
    non_empty_lines = [line for line in lines if line]

    # Join the non-empty lines back into a single string
    cleaned_text = '\n'.join(non_empty_lines)

    with open(file_path, 'w') as file:
        file.write(cleaned_text)


def process_directory(directory_path):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".java"):
                file_path = os.path.join(root, file)
                clean_text(file_path)


if __name__ == "__main__":
    current_directory = "C:\\Users\\karlt\\thesis\\datasets\\mini-testing\\src\\testcases"  # os.getcwd()
    process_directory(current_directory)
    print("Script completed successfully.")
