from BaseLlmRunner import BaseLlmRunner
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain.callbacks import get_openai_callback
import time


class SimplePromptRunner(BaseLlmRunner):
    def __init__(self, file_path, prompt_name):
        super().__init__(file_path, prompt_name)

    def run_prompt(self):
        template = self.load_prompt_from_file()
        code = self.load_file_content()
        prompt = PromptTemplate.from_template(template)
        chain = LLMChain(llm=self.llm, prompt=prompt, verbose=True)

        result = ""
        tokens_used = ""
        cost = ""
        time_spent = ""
        with get_openai_callback() as cb:
            start = time.time()
            result = chain.run({"code": code})
            end = time.time()
            tokens_used = f"total_tokens: {cb.total_tokens}, completion_tokens: {cb.completion_tokens}, prompt_tokens: {cb.prompt_tokens}"
            cost = cb.total_cost
            time_spent = f"{str(end - start)}s"
            print(f"time: {time_spent}")
            print(f"cb: {cb}")
            print(result)

        cwes = self.clean_result(result)
        with open("results.csv", "a") as res:
            res.write(f"{self.prompt_name}; {self.get_file_name()}; {cwes}; {time_spent}; {tokens_used}; {cost}\n")

        with open(self.result_folder_path + "\\" + self.get_file_name(), "w") as r:
            r.write(result)

        return result

    @staticmethod
    def clean_result(result):
        cwe_words = []
        for word in result.split():
            if "cwe" in word.lower():
                cleaned_word = word.replace(":", "").replace(",", "").replace(";", "")
                if cleaned_word not in cwe_words:
                    cwe_words.append(cleaned_word)
        return " ".join(cwe_words)
