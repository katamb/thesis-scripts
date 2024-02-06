from BaseLlmRunner import BaseLlmRunner
from langchain_community.callbacks import get_openai_callback
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain
import threading
import time
import os


class SelfReflectionPromptRunner(BaseLlmRunner):
    def __init__(self, file_path, prompt_name, lock=threading.Lock()):
        super().__init__(file_path, prompt_name, lock)
        self.self_reflection_prompt_name = self.prompt_name + "_improve"
        self.self_reflection_result_folder_path = os.path.join(self.base_result_path, self.self_reflection_prompt_name)
        if not os.path.exists(self.self_reflection_result_folder_path):
            os.makedirs(self.self_reflection_result_folder_path, exist_ok=True)

    def run_prompt(self):
        self.validate()
        conversation = ConversationChain(llm=self.llm)
        code = self.load_file_content()

        ## first call ##
        first_template = self.load_prompt_from_file(self.prompt_name)
        first_prompt = PromptTemplate.from_template(template=first_template, partial_variables={"code": code})
        with get_openai_callback() as cb1:
            start = time.time()
            llm_response_1 = conversation.predict(input=first_prompt.format_prompt().text)
            end = time.time()
            total_tokens_1 = cb1.total_tokens
            completion_tokens_1 = cb1.completion_tokens
            prompt_tokens_1 = cb1.prompt_tokens
            cost_1 = self.calculate_cost(cb1.prompt_tokens, cb1.completion_tokens)  # cb1.total_cost
            time_spent_1 = end - start
            print(llm_response_1)

        tokens_used_1 = f"total_tokens: {total_tokens_1}, completion_tokens: {completion_tokens_1}, prompt_tokens: {prompt_tokens_1}"
        cwes = self.clean_result(llm_response_1)
        self.save_result_row(self.prompt_name, len(cwes) != 0, cwes, time_spent_1, tokens_used_1, cost_1)

        with open(os.path.join(self.result_folder_path, self.get_file_name()), "w") as r:
            r.write(llm_response_1)

        ## second call ##
        second_template = self.load_prompt_from_file(self.self_reflection_prompt_name)
        second_prompt = PromptTemplate.from_template(second_template)
        with get_openai_callback() as cb2:
            start = time.time()
            llm_response_2 = conversation.predict(input=second_prompt.format_prompt().text)
            end = time.time()
            total_tokens_2 = cb2.total_tokens
            completion_tokens_2 = cb2.completion_tokens
            prompt_tokens_2 = cb2.prompt_tokens
            cost_2 = self.calculate_cost(cb2.prompt_tokens, cb2.completion_tokens)  # cb2.total_cost
            time_spent_2 = end - start
            print(llm_response_2)

        tokens_used_sum = (f"total_tokens: {self.safe_int_addition(total_tokens_1, total_tokens_2)}, "
                           f"completion_tokens: {self.safe_int_addition(completion_tokens_1, completion_tokens_2)}, "
                           f"prompt_tokens: {self.safe_int_addition(prompt_tokens_1, prompt_tokens_2)}")
        is_vulnerable = True
        cwe_ids = self.get_cwes(llm_response_2)
        if cwe_ids == "":
            is_vulnerable = False
        time_spent_sum = self.safe_float_addition(time_spent_1, time_spent_2)
        cost_sum = self.safe_float_addition(cost_1, cost_2)
        self.save_result_row(self.self_reflection_prompt_name, is_vulnerable, cwe_ids, time_spent_sum, tokens_used_sum, cost_sum)

        with open(os.path.join(self.self_reflection_result_folder_path, self.get_file_name()), "w") as r:
            r.write(llm_response_2)

        return llm_response_2

    @staticmethod
    def safe_int_addition(str_1, str_2):
        return str(int(str_1) + int(str_2))

    @staticmethod
    def safe_float_addition(str_1, str_2):
        return str(float(str_1) + float(str_2))

    def get_cwes(self, input_text):
        vulnerabilities = ""
        if "\n" in input_text:
            for line in input_text.split("\n"):
                if line.strip().startswith("vulnerability: YES |"):
                    vulnerabilities += self.clean_result(line.strip()) + " "
        else:
            if input_text.strip().startswith("vulnerability: YES |"):
                vulnerabilities += self.clean_result(input_text.strip()) + " "

        return vulnerabilities.strip()

    def validate(self):
        first_template = self.load_prompt_from_file(self.prompt_name)
        second_template = self.load_prompt_from_file(self.self_reflection_prompt_name)
        if first_template == "" or second_template == "":
            raise Exception("One of the templates is not defined!")
