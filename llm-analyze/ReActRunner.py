from BaseLlmRunner import BaseLlmRunner
from langchain import hub
from langchain_community.callbacks import get_openai_callback
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from datetime import date
from AstTool import get_ast_from_code, get_ast_from_file
from ScatTool import get_file_static_analysis
from langchain.agents import Tool
from langchain_experimental.utilities import PythonREPL
import time


# https://python.langchain.com/docs/modules/agents/agent_types/react
class ReActRunner(BaseLlmRunner):
    def __init__(self, file_path, prompt_name):
        super().__init__(file_path, prompt_name)

    def run_prompt(self):
        # Create prompt containing instructions and code
        og_prompt = hub.pull("hwchase17/react-chat")
        template = self.load_prompt_from_file(self.prompt_name)
        #prompt = PromptTemplate.from_template(template)
        code = self.load_file_content()
        prompt = (template.replace("{code}", code)
                  .replace("{file_name}", self.get_file_name()))

        # Make following tools available
        # You can create the tool to pass to an agent
        python_repl = PythonREPL()
        repl_tool = Tool(
            name="python_repl",
            description="A Python shell. Use this to execute python commands. Input should be a valid python command. If you want to see the output of a value, you should print it out with `print(...)`.",
            func=python_repl.run,
        )
        tools = [repl_tool, get_file_static_analysis, get_ast_from_code] # todo this does not work. The other one where code was provided worked better. Potentially pre-load this data? + add scat retriavl tool

        with get_openai_callback() as cb:
            # Create react agent
            agent = create_react_agent(self.llm, tools, og_prompt)
            # Create an agent executor by passing in the agent and tools
            agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
            # Make calls
            start = time.time()
            llm_response = agent_executor.invoke({"input": prompt, "chat_history": ""})
            end = time.time()
            tokens_used = f"total_tokens: {cb.total_tokens}, completion_tokens: {cb.completion_tokens}, prompt_tokens: {cb.prompt_tokens}"
            cost = cb.total_cost
            time_spent = end - start
            print(llm_response)

        with open("results.csv", "a") as res:
            cwes = self.clean_result(llm_response["output"])
            res.write(
                f"{self.model_name};"
                f"{self.dataset_name};"
                f"{self.prompt_name};"
                f"{self.get_file_name()};"
                f"{len(cwes) != 0};"
                f"{cwes};"
                f"{time_spent};"
                f"{tokens_used};"
                f"{cost};"
                f"{str(date.today())}\n"
            )

        with open(self.result_folder_path + "\\" + self.get_file_name(), "w") as r:
            r.write(llm_response["output"])

        return llm_response
