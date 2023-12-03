from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain


if __name__ == "__main__":
    template = "You are a naming consultant for new companies. What is a good name for a {company} that makes {product}?"

    prompt = PromptTemplate.from_template(template)
    llm = OpenAI(temperature=0, model_name="gpt-4-1106-preview")

    chain = LLMChain(llm=llm, prompt=prompt)

    print(chain.run({"company": "ABC Startup", "product": "colorful socks"}))
