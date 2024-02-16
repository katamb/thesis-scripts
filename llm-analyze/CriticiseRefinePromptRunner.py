from typing import List, Tuple
from BaseLlmRunner import BaseLlmRunner
from langchain_community.callbacks import get_openai_callback
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import threading
import time
import os


class CriticiseRefinePromptRunner(BaseLlmRunner):
    """
    The original prompt should be the same, but have a different file name, so we wouldn't overwrite previous results.
    Examples:
        CriticiseRefinePromptRunner(file, "basic_prompt_rci", [("basic_prompt_rci_criticise", "basic_prompt_rci_improve")])
        CriticiseRefinePromptRunner(file, "basic_prompt_refinement", [("basic_prompt_refinement_feedback", "basic_prompt_refinement_refine")])
    """

    def __init__(self,
                 file_path: str,
                 initial_prompt: str,
                 improvement_prompts: List[Tuple[str, str]],
                 lock: threading.Lock = threading.Lock()
                 ):
        super().__init__(file_path, initial_prompt, lock)
        self.improvement_prompts = improvement_prompts

    def get_folder_path(self, prompt_name):
        folder_path = os.path.join(self.base_result_path, prompt_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path, exist_ok=True)
        return folder_path

    @staticmethod
    def call_llm(chain: LLMChain, code: str) -> Tuple[str, float, int, int, int, float]:
        with get_openai_callback() as cb:
            start = time.time()
            llm_response = chain.invoke(input={"code": code})
            end = time.time()
            total_tokens = cb.total_tokens
            completion_tokens = cb.completion_tokens
            prompt_tokens = cb.prompt_tokens
            cost = cb.total_cost
            time_spent = end - start
            print(llm_response)
        return llm_response["text"], time_spent, total_tokens, completion_tokens, prompt_tokens, cost

    def run_prompt(self):
        self.validate()  # Fail early if something is not properly defined
        code = self.load_file_content()  # Load the code sample from dataset
        initial_human_input = self.load_prompt_from_file(self.prompt_name)
        initial_template = f"""The following is a conversation between a human and an AI security analyst. If the AI security analyst does not know the answer to a question, it truthfully says it does not know.\n
Human: {initial_human_input}
AI: """

        ## initial call ##
        initial_prompt = PromptTemplate(input_variables=["code"], template=initial_template)
        initial_chain = LLMChain(llm=self.llm, prompt=initial_prompt)
        llm_response_1, time_spent_1, total_tokens_1, completion_tokens_1, prompt_tokens_1, cost_1 = self.call_llm(initial_chain, code)
        # save first call results
        tokens_used_1 = f"total_tokens: {total_tokens_1}, completion_tokens: {completion_tokens_1}, prompt_tokens: {prompt_tokens_1}"
        cwes = self.get_cwes(llm_response_1)
        self.save_result_row(self.prompt_name, len(cwes.strip()) != 0, cwes, time_spent_1, tokens_used_1, cost_1)
        # save first call LLM response for audit trail
        with open(os.path.join(self.result_folder_path, self.get_file_name()), "w") as r:
            r.write(llm_response_1)

        ## second and third calls ##
        for criticise_prompt_name, improve_prompt_name in self.improvement_prompts:
            # second call
            criticise_template = initial_template + llm_response_1 + "\nHuman: " + self.load_prompt_from_file(criticise_prompt_name) + "\nAI: "
            criticise_prompt = PromptTemplate(input_variables=["code"], template=criticise_template)
            criticise_chain = LLMChain(llm=self.llm, prompt=criticise_prompt)
            llm_response_2, time_spent_2, total_tokens_2, completion_tokens_2, prompt_tokens_2, cost_2 = self.call_llm(criticise_chain, code)
            # save second call LLM response for audit trail
            with open(os.path.join(self.get_folder_path(criticise_prompt_name), self.get_file_name()), "w") as r:
                r.write(llm_response_2)

            # third (and final) call
            improve_template = criticise_template + llm_response_2 + "\nHuman: " + self.load_prompt_from_file(improve_prompt_name) + "\nAI: "
            improve_prompt = PromptTemplate(input_variables=["code"], template=improve_template)
            improve_chain = LLMChain(llm=self.llm, prompt=improve_prompt)
            llm_response_3, time_spent_3, total_tokens_3, completion_tokens_3, prompt_tokens_3, cost_3 = self.call_llm(improve_chain, code)
            # save third call results
            tokens_used_sum = (f"total_tokens: {self.safe_int_addition(total_tokens_1, total_tokens_2, total_tokens_3)}, "
                               f"completion_tokens: {self.safe_int_addition(completion_tokens_1, completion_tokens_2, completion_tokens_3)}, "
                               f"prompt_tokens: {self.safe_int_addition(prompt_tokens_1, prompt_tokens_2, prompt_tokens_3)}")
            is_vulnerable = True
            cwe_ids = self.get_cwes(llm_response_3)
            if cwe_ids.strip() == "":
                is_vulnerable = False
            time_spent_sum = self.safe_float_addition(time_spent_1, time_spent_2, time_spent_3)
            cost_sum = self.safe_float_addition(cost_1, cost_2, cost_3)
            self.save_result_row(improve_prompt_name, is_vulnerable, cwe_ids, time_spent_sum, tokens_used_sum, cost_sum)
            # save third call LLM response for audit trail
            with open(os.path.join(self.get_folder_path(improve_prompt_name), self.get_file_name()), "w") as r:
                r.write(llm_response_3)

        return llm_response_3

    @staticmethod
    def safe_int_addition(str_1, str_2, str_3):
        return str(int(str_1) + int(str_2) + int(str_3))

    @staticmethod
    def safe_float_addition(str_1, str_2, str_3):
        return str(float(str_1) + float(str_2) + float(str_3))

    def get_cwes(self, input_text):
        vulnerabilities = ""
        if "\n" in input_text:
            for line in input_text.split("\n"):
                if "vulnerability: YES |" in line.strip():
                    vulnerabilities += self.clean_result(line.strip()) + " "
        else:
            if "vulnerability: YES |" in input_text.strip():
                vulnerabilities += self.clean_result(input_text.strip()) + " "

        return vulnerabilities.strip()

    def validate(self):
        for criticise_prompt, improve_prompt in self.improvement_prompts:
            c_template = self.load_prompt_from_file(criticise_prompt)
            i_template = self.load_prompt_from_file(improve_prompt)
            if c_template.strip() == "" or i_template.strip() == "":
                raise Exception("One of the templates is not defined!")
