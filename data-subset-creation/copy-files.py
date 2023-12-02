import os
import shutil


def process_file(root, file_path):
    new_root = root.replace("Java Juliet 1.3", "mini-testing")
    new_path = file_path.replace("Java Juliet 1.3", "mini-testing")

    #answer = str(input("Copying " + file_path + " to " + new_path + ". Continue?"))
    #if answer != "yes":
    #    return

    os.makedirs(new_root, exist_ok=True)
    shutil.copy(file_path, new_path)


def process_directory(directory_path):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if "build.xml" == file or "copy-files.py" == file or "antbuild" in root:
                continue
            if "CWE" not in file or "_01" in file:
                file_path = os.path.join(root, file)
                process_file(root, file_path)


"""
Run through all files in subdirectories and copy the lines not starting with 
"""
if __name__ == "__main__":
    current_directory = "C:\\Users\\karlt\\thesis\\datasets\\Java Juliet 1.3\\src\\testcases"  # os.getcwd()
    process_directory(current_directory)
    print("Script completed successfully.")
