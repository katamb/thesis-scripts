from BaseLlmRunner import BaseLlmRunner
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_community.callbacks import get_openai_callback
from langchain.chains import ConversationChain
import time
import threading


class TestGenerator(BaseLlmRunner):
    def __init__(self, file_path, prompt_name, cwe_id, test_name, lock=threading.Lock()):
        super().__init__(file_path, prompt_name, lock)
        self.cwe_id = cwe_id
        self.test_name = test_name
        self.conversation = ConversationChain(llm=self.llm)

    def load_file_content(self):
        with open(self.file_path, 'r') as file:
            content = file.readlines()

        for i, line in enumerate(content):  # remove whitespace to save on tokens
            content[i] = line.strip()
        return "\n".join(content)

    def run_prompt(self):
        io_class="""public class IO {
public static final Logger logger = Logger.getLogger("testcases");
public static void writeString(String str) {
System.out.print(str);
}
public static void writeLine(String line) {
System.out.println(line);
}
public static void writeLine(int intNumber) {
writeLine(String.format("%02d", intNumber));
}
public static void writeLine(long longNumber) {
writeLine(String.format("%02d", longNumber));
}
public static void writeLine(double doubleNumber) {
writeLine(String.format("%02f", doubleNumber));
}
public static void writeLine(float floatNumber) {
writeLine(String.format("%02f", floatNumber));
}
public static void writeLine(short shortNumber) {
writeLine(String.format("%02d", shortNumber));
}
public static void writeLine(byte byteHex) {
writeLine(String.format("%02x", byteHex));
}
public static final boolean STATIC_FINAL_TRUE = true;
public static final boolean STATIC_FINAL_FALSE = false;
public static final int STATIC_FINAL_FIVE = 5;
public static boolean staticTrue = true;
public static boolean staticFalse = false;
public static int staticFive = 5;
public static boolean staticReturnsTrue() {
return true;
}
public static boolean staticReturnsFalse() {
return false;
}
public static boolean staticReturnsTrueOrFalse() {
return (new java.util.Random()).nextBoolean();
}
}"""
        template = self.load_prompt_from_file(self.prompt_name)
        code = self.load_file_content()
        prompt = PromptTemplate.from_template(template=template, partial_variables={"code": code, "cwe-id": self.cwe_id, "test-name": self.test_name, "io-class": io_class})

        with get_openai_callback() as cb:
            start = time.time()
            llm_response = self.conversation.predict(input=prompt.format_prompt().text)
            end = time.time()
            tokens_used = f"total_tokens: {cb.total_tokens}, completion_tokens: {cb.completion_tokens}, prompt_tokens: {cb.prompt_tokens}"
            cost = self.calculate_cost(cb.prompt_tokens, cb.completion_tokens) #cb.total_cost
            time_spent = end - start

        print("Data:", self.prompt_name, time_spent, tokens_used, cost)

        print("LLM generated tests", llm_response)
        return llm_response

    def run_additional_prompt(self, improvement_prompt):
        #template = self.load_prompt_from_file(improvement_prompt)
        #prompt = PromptTemplate.from_template(template=template)

        with get_openai_callback() as cb:
            start = time.time()
            llm_response = self.conversation.predict(input=improvement_prompt)
            end = time.time()
            tokens_used = f"total_tokens: {cb.total_tokens}, completion_tokens: {cb.completion_tokens}, prompt_tokens: {cb.prompt_tokens}"
            cost = self.calculate_cost(cb.prompt_tokens, cb.completion_tokens) #cb.total_cost
            time_spent = end - start

        print("Data:", self.prompt_name, time_spent, tokens_used, cost)

        print("LLM generated tests", llm_response)
        return llm_response
