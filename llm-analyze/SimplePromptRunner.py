from BaseLlmRunner import BaseLlmRunner
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_community.callbacks import get_openai_callback
import os
import time
import threading


class SimplePromptRunner(BaseLlmRunner):
    def __init__(self, file_path, prompt_name, lock=threading.Lock()):
        super().__init__(file_path, prompt_name, lock)

    def run_prompt(self):
        template = self.load_prompt_from_file(self.prompt_name)
        code = self.load_file_content()
        prompt = PromptTemplate.from_template(template)
        chain = LLMChain(llm=self.llm, prompt=prompt)

        with get_openai_callback() as cb:
            start = time.time()
            llm_response = chain.invoke({"code": code})["text"]
            end = time.time()
            tokens_used = f"total_tokens: {cb.total_tokens}, completion_tokens: {cb.completion_tokens}, prompt_tokens: {cb.prompt_tokens}"
            cost = cb.total_cost
            time_spent = end - start
            print(llm_response)

        cwes = self.get_cwes(llm_response)
        self.save_result_row(self.prompt_name, len(cwes) != 0, cwes, time_spent, tokens_used, cost)

        with open(os.path.join(self.result_folder_path, self.get_file_name()), "w") as r:
            r.write(llm_response)

        return llm_response
