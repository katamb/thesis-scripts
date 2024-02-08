from BaseLlmRunner import BaseLlmRunner
from langchain_community.callbacks import get_openai_callback
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from tools.AstTool import get_ast_from_code
#from langchain.agents import Tool
from tools.ScatTool import get_codeql_results, get_spotbugs_results
from langchain_experimental.tools import PythonREPLTool
#from langchain_experimental.utilities import PythonREPL
from langchain_core.runnables import RunnableConfig
import time
import threading
import os


# https://python.langchain.com/docs/modules/agents/agent_types/react
class ReActRunner(BaseLlmRunner):
    def __init__(self, file_path, prompt_name, lock=threading.Lock()):
        super().__init__(file_path, prompt_name, lock)

    def run_prompt(self):
        # Create prompt containing instructions and code
        template = self.load_prompt_from_file(self.prompt_name)
        prompt = PromptTemplate.from_template(template)
        code = self.load_file_content()
        #prompt = hub.pull("hwchase17/react")

        # Make following tools available
        tools = [PythonREPLTool(), get_codeql_results, get_spotbugs_results, get_ast_from_code]  # todo ast does not always work

        # todo callback not working atm
        with get_openai_callback() as cb:
            # Create react agent
            agent = create_react_agent(self.llm, tools, prompt)
            # Create an agent executor by passing in the agent and tools
            agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
            # Make calls
            start = time.time()
            llm_response = agent_executor.invoke({"input": code}, config=RunnableConfig(callbacks=[cb]), include_run_info=True, verbose=True)
            end = time.time()
            tokens_used = f"total_tokens: {cb.total_tokens}, completion_tokens: {cb.completion_tokens}, prompt_tokens: {cb.prompt_tokens}"
            cost = cb.total_cost
            time_spent = end - start
            print(llm_response)

        cwes = self.clean_result(llm_response["output"])
        self.save_result_row(self.prompt_name, len(cwes) != 0, cwes, time_spent, tokens_used, cost)

        with open(os.path.join(self.result_folder_path, self.get_file_name()), "w") as r:
            r.write(llm_response["output"])

        return llm_response
