from dotenv import load_dotenv, find_dotenv
from abc import abstractmethod
from langchain_openai import ChatOpenAI
from langchain.globals import set_verbose
import os
import re


class BaseLlmRunner:
    def __init__(self, file_path, prompt_name):
        load_dotenv(find_dotenv())
        self.dataset_name = os.environ.get("CURRENT_DATASET_NAME")
        self.file_path = file_path
        self.prompt_name = prompt_name
        self.model_name = "gpt-4-1106-preview"
        self.llm = ChatOpenAI(temperature=0, model_name=self.model_name)
        set_verbose(True)
        self.base_result_path = os.environ.get('RESULTS_DIRECTORY_ROOT') + "\\" + self.dataset_name + "\\"
        self.result_folder_path = self.base_result_path + self.prompt_name
        if not os.path.exists(self.result_folder_path):
            os.makedirs(self.result_folder_path)

    def load_file_content(self):
        with open(self.file_path, 'r') as file:
            content = file.readlines()
        content[0] = "package com.bank.service;\n"  # remove package name to avoid leaking clues to LLM

        for i, line in enumerate(content):  # remove whitespace to save on tokens
            content[i] = line.strip()
        return "\n".join(content)

    def get_file_name(self):
        last_slash_index = self.file_path.rindex('\\') + 1
        last_dot_index = self.file_path.rindex('.')
        file_name = self.file_path[last_slash_index:last_dot_index]
        return file_name

    @staticmethod
    def load_prompt_from_file(prompt_name):
        with open("./prompts/" + prompt_name, 'r') as file:
            content = file.read()
        return content

    @staticmethod
    def clean_result(text):
        pattern = r'\b(?:cwe-|CWE-|cwe|CWE)(\d+)\b'
        matches = re.findall(pattern, text, re.IGNORECASE)
        unique_matches = set(matches)
        formatted_matches = [f'CWE-{match}' for match in unique_matches]
        return " ".join(formatted_matches)

    @abstractmethod
    def run_prompt(self):
        pass
