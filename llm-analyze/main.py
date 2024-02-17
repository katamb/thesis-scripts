from dotenv import load_dotenv, find_dotenv
from SimplePromptRunner import SimplePromptRunner
#from ReActRunner import ReActRunner
#from SelfReflectionPromptRunner import SelfReflectionPromptRunner
from CriticiseRefinePromptRunner import CriticiseRefinePromptRunner
from concurrent.futures import ThreadPoolExecutor
from tools.ast.ApiCallExtractor import get_api_call_seq
import os
import threading


def run_prompt(file_path: str, lock=threading.Lock()):
    runner = CriticiseRefinePromptRunner(file_path,
                                         "api_seq_prompt_rci",
                                         [
                                             ("api_seq_prompt_rci_criticise_short", "api_seq_prompt_rci_improve_short")
                                         ],
                                         lock)
    #runner = SimplePromptRunner(file_path, "cot_high_level", lock)
    runner.run_prompt()


def process_directory_concurrently(directory_path: str):
    lock = threading.Lock()
    counter = 0
    for root, dirs, files in os.walk(directory_path):
        with ThreadPoolExecutor(max_workers=17) as executor:
            futures = []
            for file in files:
                if "Main" in file or "Helper" in file:
                    continue
                elif file.startswith("J") and file.endswith(".java") and file not in ["J10126.java","J10126.java","J10127.java","J10127.java","J10530.java","J10530.java","J10531.java","J10531.java","J10676.java","J10676.java","J10677.java","J10677.java","J10738.java","J10738.java","J10739.java","J10739.java","J10754.java","J10754.java","J10755.java","J10755.java","J11014.java","J11014.java","J11015.java","J11015.java","J12224.java","J12224.java","J12225.java","J12225.java","J12290.java","J12290.java","J12291.java","J12291.java","J12326.java","J12326.java","J12327.java","J12327.java","J12498.java","J12498.java","J12499.java","J12499.java","J12752.java","J12752.java","J12753.java","J12753.java","J12930.java","J12930.java","J12931.java","J12931.java","J13100.java","J13100.java","J13101.java","J13101.java"]:
                    file_path = os.path.join(root, file)
                    counter += 1
                    print("x-count", counter)
                    future = executor.submit(run_prompt, file_path, lock)
                    futures.append(future)

            # Wait for all tasks to complete
            for future in futures:
                future.result()

def load_file_content(file_path):
    with open(file_path, 'r') as file:
        content = file.readlines()
    for i, line in enumerate(content):  # remove whitespace to save on tokens
        content[i] = line.strip()
    return "\n".join(content)

def process_directory(directory_path: str):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if "Main" in file or "Helper" in file:
                continue
            elif file.startswith("J") and file.endswith(".java"):
                file_path = os.path.join(root, file)
                code = load_file_content(file_path)
                print("---file", file)
                get_api_call_seq(code)
                print("--------")
                #run_prompt(file_path)


if __name__ == "__main__":
    load_dotenv(find_dotenv())
    dataset_root = os.environ.get("DATASET_DIRECTORY_ROOT")

    # C:\Users\karlt\thesis\datasets\juliet-top-25\src\testcases\CWE129_Improper_Validation_of_Array_Index\s03\J11608.java
    #file = os.path.join(dataset_root, "src", "testcases", "CWE129_Improper_Validation_of_Array_Index", "s03", "J11608.java")
    #run_prompt(file)

    folder = os.path.join(dataset_root, "src", "testcases")
    #process_directory_concurrently(folder)
    process_directory(folder)
