from dotenv import load_dotenv, find_dotenv
from abc import abstractmethod
from langchain_openai import ChatOpenAI
from langchain.globals import set_verbose
from datetime import date
import os
import re


class BaseLlmRunner:
    def __init__(self, file_path, prompt_name, results_lock):
        """
        :param file_path: The code file path, which should contain the code to be analysed.
        :param prompt_name: The prompt name.
        :param results_lock: Not required, but providing a lock is highly encouraged if running in multiple threads.
        """
        load_dotenv(find_dotenv())
        self.dataset_name = os.environ.get("CURRENT_DATASET_NAME")
        self.file_path = file_path
        self.prompt_name = prompt_name
        self.model_name = "gpt-4-0125-preview"
        self.llm = ChatOpenAI(temperature=0, model_name=self.model_name, streaming=False)
        self.results_lock = results_lock
        set_verbose(True)
        self.base_result_path = os.environ.get('RESULTS_DIRECTORY_ROOT') + "\\" + self.dataset_name + "\\"
        self.result_folder_path = self.base_result_path + self.prompt_name
        if not os.path.exists(self.result_folder_path):
            os.makedirs(self.result_folder_path, exist_ok=True)

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

    # Workaround until langchain supports new gpt-4-turbo model
    def calculate_cost(self, prompt_tokens, completion_tokens):
        if self.model_name != "gpt-4-0125-preview":
            raise Exception("Check model")
        return ((prompt_tokens * 0.01) + (completion_tokens * 0.03)) * 0.001

    def save_result_row(self, prompt_name, is_vulnerable, cwe_ids, timing, tokens_used, cost):
        with self.results_lock:
            with open("results.csv", "a") as res:
                res.write(
                    f"{self.model_name};"
                    f"{self.dataset_name};"
                    f"{prompt_name};"
                    f"{self.get_file_name()};"
                    f"{is_vulnerable};"
                    f"{cwe_ids};"
                    f"{timing};"
                    f"{tokens_used};"
                    f"{cost};"
                    f"{str(date.today())}\n"
                )

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
