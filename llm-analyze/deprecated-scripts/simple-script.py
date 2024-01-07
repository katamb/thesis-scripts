from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain


def load_file(file_path):
    with open(file_path, 'r') as file:
        content = file.readlines()
    content[0] = "package com.bank.service;\n"  # remove package name to avoid leaking clues to LLM
    return "".join(content)


def run_prompt(template, code):
    prompt = PromptTemplate.from_template(template)
    llm = OpenAI(temperature=0, model_name="gpt-4-1106-preview")

    chain = LLMChain(llm=llm, prompt=prompt, verbose=True)

    return chain.run({"code": code})


def persist_result(file_path):

    pass


def get_file_name(file_path):
    last_dot_index = file_path.rindex('.')
    last_slash_index = file_path.rindex('\\') + 1
    file_name = file_path[last_slash_index:last_dot_index]
    return file_name


if __name__ == "__main__":
    noever_template = """Act as the world's greatest static code analyzer for java programming language. 
    I will give you a code snippet, and you will identify the language and analyze it for vulnerabilities. 
    Give the output in a format: filename, vulnerabilities detected as a numbered list, and proposed fixes as a separate numbered list.
    ---
    {code}
    """
    noever_modified_template = """Act as the world's greatest static code analyzer for java programming language. 
    I will give you a code snippet, and you will identify the language and analyze it for vulnerabilities. 
    Give the output in a format: vulnerability: <YES or NO> | vulnerability type: <CWE_ID> | vulnerability name: <NAME_OF_CWE> | explanation: <explanation for prediction>
    ---
    {code}
    """
    file_path = "C:\\Users\\karlt\\thesis\\datasets\\mini-testing\\src\\testcases\\CWE23_Relative_Path_Traversal\\J1774.java"
    code_file = load_file(file_path)

    #print(code_file)

    result = run_prompt(noever_template, code_file)
    persist_result(result)
    print(result)
