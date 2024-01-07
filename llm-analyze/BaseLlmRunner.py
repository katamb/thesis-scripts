from abc import abstractmethod
from langchain.chat_models import ChatOpenAI
import os


class BaseLlmRunner:
    def __init__(self, file_path, prompt_name):
        self.file_path = file_path
        self.prompt_name = prompt_name
        self.llm = ChatOpenAI(temperature=0, model_name="gpt-4-1106-preview")
        self.base_result_path = "C:\\Users\\karlt\\thesis\\datasets\\mini-testing-results\\"
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
    def clean_result(result):
        cwe_words = []
        for word in result.split():
            if "cwe" in word.lower():
                cleaned_word = word.replace(":", "").replace(",", "").replace(";", "")
                if cleaned_word not in cwe_words:
                    cwe_words.append(cleaned_word)
        return " ".join(cwe_words)

    @abstractmethod
    def run_prompt(self):
        pass
