from BaseLlmRunner import BaseLlmRunner
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_community.callbacks import get_openai_callback
from datetime import date
import time


class SimplePromptRunner(BaseLlmRunner):
    def __init__(self, file_path, prompt_name):
        super().__init__(file_path, prompt_name)

    def run_prompt(self):
        template = self.load_prompt_from_file(self.prompt_name)
        code = self.load_file_content()
        prompt = PromptTemplate.from_template(template)
        chain = LLMChain(llm=self.llm, prompt=prompt)

        with get_openai_callback() as cb:
            start = time.time()
            llm_response = chain.run({"code": code})
            end = time.time()
            tokens_used = f"total_tokens: {cb.total_tokens}, completion_tokens: {cb.completion_tokens}, prompt_tokens: {cb.prompt_tokens}"
            cost = cb.total_cost
            time_spent = end - start
            print(llm_response)

        with open("results.csv", "a") as res:
            cwes = self.clean_result(llm_response)
            res.write(
                f"{self.model_name};"
                f"{self.dataset_name};"
                f"{self.prompt_name};"
                f"{self.get_file_name()};"
                f"{len(cwes) != 0};"
                f"{cwes};"
                f"{time_spent};"
                f"{tokens_used};"
                f"{cost};"
                f"{str(date.today())}\n"
            )

        with open(self.result_folder_path + "\\" + self.get_file_name(), "w") as r:
            r.write(llm_response)

        return llm_response
