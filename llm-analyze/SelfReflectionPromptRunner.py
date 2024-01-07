from BaseLlmRunner import BaseLlmRunner
from langchain.callbacks import get_openai_callback
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain
import time


class SelfReflectionPromptRunner(BaseLlmRunner):
    def __init__(self, file_path, prompt_name):
        super().__init__(file_path, prompt_name)

    def run_prompt(self):
        conversation = ConversationChain(llm=self.llm, verbose=True)
        code = self.load_file_content()

        first_template = """
You are a security researcher, expert in detecting security vulnerabilities. Carefully analyze the given code snippet 
and track the data flows from various sources to sinks. Assume that any call to an unknown external API is unsanitized. 
Please provide a response only in the following format: 
Here is a data flow analysis of the given code snippet: 
A. Sources: <numbered list of input sources> 
B. Sinks: <numbered list of output sinks> 
C. Sanitizers: <numbered list of sanitizers, if any> 
D. Unsanitized Data Flows: <numbered list of data flows that are not sanitized in the format (source, sink, why this flow could be vulnerable)> 
E. Vulnerability analysis verdict: vulnerability: <YES or NO> | vulnerability type: <CWE_ID> | vulnerability name: <NAME_OF_CWE> | explanation: <explanation for prediction>
Is the following code snippet prone to any security vulnerability? ```{code}```
"""
        first_prompt = PromptTemplate.from_template(template=first_template, partial_variables={"code": code})
        with get_openai_callback() as cb1:
            start = time.time()
            llm_response_1 = conversation.predict(input=first_prompt.format_prompt().text)
            end = time.time()
            print(f"time: {str(end - start)} s")
            print(f"cd: {cb1}")
            print(llm_response_1)

        second_template = """
Is this analysis correct? Return your response in the following format: Yes / No explanation: <reason for the analysis being correct or wrong> Final Vulnerability analysis verdict: vulnerability: <YES or NO> | vulnerability type: <CWE_ID>
"""
        second_prompt = PromptTemplate.from_template(second_template)
        with get_openai_callback() as cb2:
            start = time.time()
            llm_response_2 = conversation.predict(input=second_prompt.format_prompt().text)
            end = time.time()
            print(f"time: {str(end - start)} s")
            print(f"cd: {cb2}")
            print(llm_response_2)

        # todo save results
        return llm_response_2

