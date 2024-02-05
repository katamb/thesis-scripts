from BaseLlmRunner import BaseLlmRunner
from langchain_community.callbacks import get_openai_callback
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain
import threading
import time
import os
import re


class CriticiseRefinePromptRunner(BaseLlmRunner):
    """
    The original prompt should be the same, but have a different file name, so we wouldn't overwrite previous results.
    Examples:
        CriticiseRefinePromptRunner(file, "basic_prompt_rci", "basic_prompt_rci_criticise", "basic_prompt_rci_improve")
        CriticiseRefinePromptRunner(file, "basic_prompt_refinement", "basic_prompt_refinement_feedback", "basic_prompt_refinement_refine")
    """
    def __init__(self, file_path, first_prompt_name, second_prompt_name, third_prompt_name, lock=threading.Lock()):
        super().__init__(file_path, first_prompt_name, lock)
        self.criticise_prompt = second_prompt_name
        self.improve_prompt = third_prompt_name
        self.criticise_folder_path = os.path.join(self.base_result_path, self.criticise_prompt)
        self.improve_folder_path = os.path.join(self.base_result_path, self.improve_prompt)
        if not os.path.exists(self.criticise_folder_path):
            os.makedirs(self.criticise_folder_path, exist_ok=True)
        if not os.path.exists(self.improve_folder_path):
            os.makedirs(self.improve_folder_path, exist_ok=True)

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

        # save first call results
        tokens_used_1 = f"total_tokens: {total_tokens_1}, completion_tokens: {completion_tokens_1}, prompt_tokens: {prompt_tokens_1}"
        cwes = self.clean_result(llm_response_1)
        self.save_result_row(self.prompt_name, len(cwes) != 0, cwes, time_spent_1, tokens_used_1, cost_1)

        # save first call LLM response for audit trail
        with open(os.path.join(self.result_folder_path, self.get_file_name()), "w") as r:
            r.write(llm_response_1)

        ## second call ##
        second_template = self.load_prompt_from_file(self.criticise_prompt)
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

        # save second call LLM response for audit trail
        with open(os.path.join(self.criticise_folder_path, self.get_file_name()), "w") as r:
            r.write(llm_response_2)

        ## third (and final) call ##
        third_template = self.load_prompt_from_file(self.improve_prompt)
        third_prompt = PromptTemplate.from_template(third_template)
        with get_openai_callback() as cb3:
            start = time.time()
            llm_response_3 = conversation.predict(input=third_prompt.format_prompt().text)
            end = time.time()
            total_tokens_3 = cb3.total_tokens
            completion_tokens_3 = cb3.completion_tokens
            prompt_tokens_3 = cb3.prompt_tokens
            cost_3 = self.calculate_cost(cb3.prompt_tokens, cb3.completion_tokens)  # cb3.total_cost
            time_spent_3 = end - start
            print(llm_response_3)

        # save third call results
        tokens_used_sum = (f"total_tokens: {self.safe_int_addition(total_tokens_1, total_tokens_2, total_tokens_3)}, "
                           f"completion_tokens: {self.safe_int_addition(completion_tokens_1, completion_tokens_2, completion_tokens_3)}, "
                           f"prompt_tokens: {self.safe_int_addition(prompt_tokens_1, prompt_tokens_2, prompt_tokens_3)}")
        is_vulnerable = self.is_vulnerability_present(llm_response_3)
        cwe_ids = self.clean_result(llm_response_3)
        if cwe_ids == "" and is_vulnerable:
            cwe_ids = self.clean_result(llm_response_1)
        time_spent_sum = self.safe_float_addition(time_spent_1, time_spent_2, time_spent_3)
        cost_sum = self.safe_float_addition(cost_1, cost_2, cost_3)
        self.save_result_row(self.improve_prompt, is_vulnerable, cwe_ids, time_spent_sum, tokens_used_sum, cost_sum)

        # save third call LLM response for audit trail
        with open(os.path.join(self.improve_folder_path, self.get_file_name()), "w") as r:
            r.write(llm_response_3)

        return llm_response_3

    @staticmethod
    def safe_int_addition(str_1, str_2, str_3):
        return str(int(str_1) + int(str_2) + int(str_3))

    @staticmethod
    def safe_float_addition(str_1, str_2, str_3):
        return str(float(str_1) + float(str_2) + float(str_3))

    def is_vulnerability_present(self, input_text):
        vulnerability_pattern = re.compile(r'vulnerability: (YES|NO) \|')

        # Write out if some manual checks are needed
        all_matches = vulnerability_pattern.findall(input_text)
        if len(all_matches) > 1:
            with open("./manual-checks-needed.csv", "a") as f:
                f.write(f"{self.dataset_name}, {self.model_name}, {self.prompt_name}")

        # Find the match, covers 99% of cases
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
        second_template = self.load_prompt_from_file(self.criticise_prompt)
        third_template = self.load_prompt_from_file(self.improve_prompt)
        if first_template.strip() == "" or second_template.strip() == "" or third_template.strip() == "":
            raise Exception("One of the templates is not defined!")
