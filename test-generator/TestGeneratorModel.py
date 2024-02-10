from BaseModel import BaseModel
from langchain_core.prompts import PromptTemplate
from langchain_community.callbacks import get_openai_callback
from langchain.chains import ConversationChain
import time
import threading


class TestGeneratorModel(BaseModel):
    def __init__(self, file_path: str, lock: threading.Lock = threading.Lock()):
        super().__init__(file_path, lock)
        self.conversation = ConversationChain(llm=self.llm)

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
        return llm_response.replace("```java", "").replace("```", "")
