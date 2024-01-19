from BaseLlmRunner import BaseLlmRunner
from langchain_community.callbacks import get_openai_callback
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain
from datetime import date
import time
import os
import re


class SelfReflectionPromptRunner(BaseLlmRunner):
    def __init__(self, file_path, prompt_name):
        super().__init__(file_path, prompt_name)
        self.self_reflection_prompt_name = self.prompt_name + "_self_reflection"
        self.self_reflection_result_folder_path = self.base_result_path + self.self_reflection_prompt_name
        if not os.path.exists(self.self_reflection_result_folder_path):
            os.makedirs(self.self_reflection_result_folder_path)

    def run_prompt(self):
        self.validate()
        conversation = ConversationChain(llm=self.llm)
        code = self.load_file_content()

        first_template = self.load_prompt_from_file(self.prompt_name)
        first_prompt = PromptTemplate.from_template(template=first_template, partial_variables={"code": code})
        with get_openai_callback() as cb1:
            start = time.time()
            llm_response_1 = conversation.predict(input=first_prompt.format_prompt().text)
            end = time.time()
            total_tokens_1 = cb1.total_tokens
            completion_tokens_1 = cb1.completion_tokens
            prompt_tokens_1 = cb1.prompt_tokens
            cost_1 = cb1.total_cost
            time_spent_1 = end - start
            print(llm_response_1)

        tokens_used = f"total_tokens: {total_tokens_1}, completion_tokens: {completion_tokens_1}, prompt_tokens: {prompt_tokens_1}"
        with open("results.csv", "a") as res:
            cwes = self.clean_result(llm_response_1)
            res.write(
                f"{self.model_name};"
                f"{self.dataset_name};"
                f"{self.prompt_name};"
                f"{self.get_file_name()};"
                f"{len(cwes) != 0};"
                f"{self.clean_result(llm_response_1)};"
                f"{time_spent_1};"
                f"{tokens_used};"
                f"{cost_1};"
                f"{str(date.today())}\n"
            )

        with open(self.result_folder_path + "\\" + self.get_file_name(), "w") as r:
            r.write(llm_response_1)

        second_template = self.load_prompt_from_file(self.self_reflection_prompt_name)
        second_prompt = PromptTemplate.from_template(second_template)
        with get_openai_callback() as cb2:
            start = time.time()
            llm_response_2 = conversation.predict(input=second_prompt.format_prompt().text)
            end = time.time()
            total_tokens_2 = cb2.total_tokens
            completion_tokens_2 = cb2.completion_tokens
            prompt_tokens_2 = cb2.prompt_tokens
            cost_2 = cb2.total_cost
            time_spent_2 = end - start
            print(llm_response_2)

        tokens_used = (f"total_tokens: {self.safe_int_addition(total_tokens_1, total_tokens_2)}, "
                       f"completion_tokens: {self.safe_int_addition(completion_tokens_1, completion_tokens_2)}, "
                       f"prompt_tokens: {self.safe_int_addition(prompt_tokens_1, prompt_tokens_2)}")
        with open("results.csv", "a") as res:
            res.write(
                f"{self.model_name};"
                f"{self.dataset_name};"
                f"{self.self_reflection_prompt_name};"
                f"{self.get_file_name()};"
                f"{self.is_vulnerability_present(llm_response_2)};"
                f"{self.clean_result(llm_response_2)};"
                f"{self.safe_float_addition(time_spent_1, time_spent_2)};"
                f"{tokens_used};"
                f"{self.safe_float_addition(cost_1, cost_2)};"
                f"{str(date.today())}\n"
            )

        with open(self.self_reflection_result_folder_path + "\\" + self.get_file_name(), "w") as r:
            r.write(llm_response_2)

        return llm_response_2

    @staticmethod
    def safe_int_addition(str_1, str_2):
        return str(int(str_1) + int(str_2))

    @staticmethod
    def safe_float_addition(str_1, str_2):
        return str(float(str_1) + float(str_2))

    @staticmethod
    def is_vulnerability_present(input_text):
        vulnerability_pattern = re.compile(r'vulnerability: (YES|NO) \|')

        vulnerability_match = vulnerability_pattern.search(input_text)

        if vulnerability_match:
            vulnerability_status = vulnerability_match.group(1).strip()
            if vulnerability_status.upper() == "YES":
                return True
            if vulnerability_status.upper() == "NO":
                return False

        return None

    def validate(self):
        first_template = self.load_prompt_from_file(self.prompt_name)
        second_template = self.load_prompt_from_file(self.prompt_name + "_self_reflection")
        if first_template == "" or second_template == "":
            raise Exception("One of the templates is not defined!")
