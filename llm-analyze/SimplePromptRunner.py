from BaseLlmRunner import BaseLlmRunner
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_community.callbacks import get_openai_callback
from utils.AnthropicTokenCounter import AnthropicTokenCounter
import os
import time
import threading


class SimplePromptRunner(BaseLlmRunner):
    def __init__(self, file_path: str, prompt_name: str, lock=threading.Lock()):
        super().__init__(file_path, prompt_name, lock)

    def run_prompt(self):
        template = self.load_prompt_from_file(self.prompt_name)
        code = self.load_file_content()
        prompt = PromptTemplate.from_template(template)
        chain = LLMChain(llm=self.llm, prompt=prompt)

        if "gpt" in self.model_name:
            llm_response, cost, time_spent, tokens_used = self.call_gpt_llm(chain, code)
        elif "claude" in self.model_name:
            llm_response, cost, time_spent, tokens_used = self.call_anthropic_llm(chain, code)
        else:
            raise Exception("Using a model not set up!")

        cwes = self.get_cwes(llm_response)
        self.save_result_row(self.prompt_name, len(cwes) != 0, cwes, time_spent, tokens_used, cost)

        with open(os.path.join(self.result_folder_path, self.get_file_name()), "w") as r:
            r.write(llm_response)

        return llm_response

    def call_gpt_llm(self, chain: LLMChain, code: str):
        with get_openai_callback() as cb:
            start = time.time()
            llm_response = chain.invoke({"code": code})["text"]
            end = time.time()
            tokens_used = f"total_tokens: {cb.total_tokens}, completion_tokens: {cb.completion_tokens}, prompt_tokens: {cb.prompt_tokens}"
            cost = cb.total_cost
            time_spent = end - start
            print(llm_response)
        return llm_response, cost, time_spent, tokens_used

    def call_anthropic_llm(self, chain: LLMChain, code: str):
        token_counter = AnthropicTokenCounter(self.llm)
        start = time.time()
        llm_response = chain.invoke({"code": code}, config={"callbacks": [token_counter]})["text"]
        end = time.time()
        completion_tokens = token_counter.output_tokens
        prompt_tokens = token_counter.input_tokens
        tokens_used = f"total_tokens: {completion_tokens + prompt_tokens}, completion_tokens: {completion_tokens}, prompt_tokens: {prompt_tokens}"
        if "opus" in self.model_name:
            cost = completion_tokens / 1000 * 0.075 + prompt_tokens / 1000 * 0.015  # This is the cost for Opus model
        else:
            raise Exception("The billing for the model is no configured!")
        time_spent = end - start
        print(llm_response)
        return llm_response, cost, time_spent, tokens_used
