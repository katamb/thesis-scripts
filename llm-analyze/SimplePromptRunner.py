from BaseLlmRunner import BaseLlmRunner
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain.callbacks import get_openai_callback
import time


class SimplePromptRunner(BaseLlmRunner):
    def __init__(self, file_path):
        super().__init__(file_path)

    def run_prompt(self):
        noever_template = """
Act as the world's greatest static code analyzer for java programming language. 
I will give you a code snippet, and you will identify the language and analyze it for vulnerabilities. 
Give the output in a format: filename, vulnerabilities detected as a numbered list, and proposed fixes as a separate numbered list.
---
{code}
"""
        code = self.load_file_content()
        prompt = PromptTemplate.from_template(noever_template)
        chain = LLMChain(llm=self.llm, prompt=prompt, verbose=True)

        with get_openai_callback() as cb:
            start = time.time()
            result = chain.run({"code": code})
            end = time.time()
            print(f"time: {str(end - start)} s")
            print(f"cd: {cb}")
            print(result)

        # todo save results
        return result
