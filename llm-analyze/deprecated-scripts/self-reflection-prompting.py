from langchain_core.messages import HumanMessage, SystemMessage
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.prompts import HumanMessagePromptTemplate, ChatPromptTemplate


def load_file(file_path):
    with open(file_path, 'r') as file:
        content = file.readlines()
    content[0] = "package com.bank.service;\n"  # remove package name to avoid leaking clues to LLM
    return "".join(content)


def run_prompt(messages, code):
    #prompt = ChatPromptTemplate.from_messages(messages=messages)
    llm = ChatOpenAI(temperature=0, model_name="gpt-4-1106-preview")
    #chain = LLMChain(llm=llm, prompt=prompt, verbose=True)

    #return chain.run({"code": code})
    return llm(messages)


def get_file_name(file_path):
    last_dot_index = file_path.rindex('.')
    last_slash_index = file_path.rindex('\\') + 1
    file_name = file_path[last_slash_index:last_dot_index]
    return file_name


if __name__ == "__main__":
    file_path = "C:\\Users\\karlt\\thesis\\datasets\\mini-testing\\src\\testcases\\CWE23_Relative_Path_Traversal\\J1774.java"
    code_file = load_file(file_path)
    prompt = PromptTemplate(
        template="Is the following code snippet prone to any security vulnerability? ```{code}```",
        input_variables=["code"]
    )
    human_message_prompt = HumanMessagePromptTemplate(prompt=prompt)
    #human_message_prompt.format(code=code_file)
    cwe_df_sr = ChatPromptTemplate.from_messages([
        SystemMessage(content="You are a security researcher, expert in detecting security vulnerabilities. Carefully analyze the given code snippet and track the data flows from various sources to sinks. Assume that any call to an unknown external API is unsanitized. Please provide a response only in the following format: Here is a data flow analysis of the given code snippet: A. Sources: <numbered list of input sources> B. Sinks: <numbered list of output sinks> C. Sanitizers: <numbered list of sanitizers, if any> D. Unsanitized Data Flows: <numbered list of data flows that are not sanitized in the format (source, sink, why this flow could be vulnerable)> E. Vulnerability analysis verdict: vulnerability: <YES or NO> | vulnerability type: <CWE_ID> | vulnerability name: <NAME_OF_CWE> | explanation: <explanation for prediction>"),
        human_message_prompt,
        HumanMessage(content="Is this analysis correct? Return your response in the following format: Yes / No explanation: <reason for the analysis being correct or wrong> Final Vulnerability analysis verdict: vulnerability: <YES or NO> | vulnerability type: <CWE_ID>"),
    ])
    chat_prompt_with_values = cwe_df_sr.format_prompt(code=code_file)

    result = run_prompt(chat_prompt_with_values.to_messages(), code_file)
    print(result)
    print(result.content)
