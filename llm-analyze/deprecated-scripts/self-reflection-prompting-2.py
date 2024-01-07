from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain, SimpleSequentialChain


def run_prompt(code):
    llm = ChatOpenAI(temperature=0, model_name="gpt-4-1106-preview")
    conversation = ConversationChain(llm=llm, verbose=True)

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
    llm_response_1 = conversation.predict(input=first_prompt.format_prompt().text)
    print(llm_response_1)

    second_template = """
Is this analysis correct? Return your response in the following format: Yes / No explanation: <reason for the analysis being correct or wrong> Final Vulnerability analysis verdict: vulnerability: <YES or NO> | vulnerability type: <CWE_ID>
"""
    second_prompt = PromptTemplate.from_template(second_template)
    llm_response_2 = conversation.predict(input=second_prompt.format_prompt().text)
    print(llm_response_2)

    return llm_response_2


def load_file(file_path):
    with open(file_path, 'r') as file:
        content = file.readlines()
    content[0] = "package com.bank.service;\n"  # remove package name to avoid leaking clues to LLM
    return "".join(content)


def get_file_name(file_path):
    last_dot_index = file_path.rindex('.')
    last_slash_index = file_path.rindex('\\') + 1
    file_name = file_path[last_slash_index:last_dot_index]
    return file_name


if __name__ == "__main__":
    file_path = "C:\\Users\\karlt\\thesis\\datasets\\mini-testing\\src\\testcases\\CWE23_Relative_Path_Traversal\\J1774.java"
    code_file = load_file(file_path)

    result = run_prompt(code_file)
    print(result)
