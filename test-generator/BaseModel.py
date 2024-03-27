from dotenv import load_dotenv, find_dotenv
from langchain.chains import ConversationChain
from langchain_openai import ChatOpenAI
from langchain.globals import set_verbose
from threading import Lock
from langchain_core.prompts import PromptTemplate
from langchain_community.callbacks import get_openai_callback
import time
import os


class BaseModel:
    def __init__(self, file_path: str, file_name: str, results_lock: Lock = Lock()):
        """
        :param file_path: The code file path, which should contain the code to be analysed.
        :param results_lock: Not required, but providing a lock is highly encouraged if running in multiple threads.
        """
        load_dotenv(find_dotenv())
        self.dataset_name = os.environ.get("CURRENT_DATASET_NAME")
        self.file_path = file_path
        self.model_name = "gpt-4-0125-preview"
        self.llm = ChatOpenAI(temperature=0, model_name=self.model_name, streaming=False)
        self.conversation = ConversationChain(llm=self.llm)
        self.results_lock = results_lock
        set_verbose(True)
        self.base_result_path = os.path.join(os.environ.get('RESULTS_DIRECTORY_ROOT'), "testgen", self.dataset_name, self.model_name, file_name)
        if not os.path.exists(self.base_result_path):
            os.makedirs(self.base_result_path, exist_ok=True)

    def save_result(self, result, prompt):
        with open(os.path.join(self.base_result_path, prompt), "a") as file:
            file.write("--------------------------------------------------------------------\n")
            file.write(result)
            file.write("--------------------------------------------------------------------\n")

    def load_file_content(self) -> str:
        with open(self.file_path, 'r') as file:
            content = file.readlines()

        for i, line in enumerate(content):  # remove whitespace to save on tokens
            content[i] = line.strip()
        return "\n".join(content)

    # Workaround until langchain supports new gpt-4-turbo model
    def calculate_cost(self, prompt_tokens, completion_tokens) -> float:
        if self.model_name != "gpt-4-0125-preview":
            raise Exception("Check model")
        return ((prompt_tokens * 0.01) + (completion_tokens * 0.03)) * 0.001

    @staticmethod
    def load_prompt_from_file(prompt_name: str) -> str:
        with open(os.path.join("prompts", prompt_name), 'r') as file:
            content = file.read()
        return content

    def run_prompt(self, prompt_name: str, variables: dict) -> str:
        template = self.load_prompt_from_file(prompt_name)
        prompt = PromptTemplate.from_template(template=template, partial_variables=variables)

        with get_openai_callback() as cb:
            start = time.time()
            llm_response = self.conversation.predict(input=prompt.format_prompt().text)
            end = time.time()
            tokens_used = f"total_tokens: {cb.total_tokens}, completion_tokens: {cb.completion_tokens}, prompt_tokens: {cb.prompt_tokens}"
            cost = self.calculate_cost(cb.prompt_tokens, cb.completion_tokens)  # cb.total_cost
            time_spent = end - start

        print("Data:", prompt_name, time_spent, tokens_used, cost)

        self.save_result(llm_response, prompt_name)
        print("LLM generated evaluation", llm_response)
        return llm_response
