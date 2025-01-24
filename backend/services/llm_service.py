from os import getenv
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI


class LLMService:
    def __init__(self):
        load_dotenv()
        self.llm = OpenAI(
            temperature=0.5,
            top_p=0.7,
            api_key=getenv("HF_TOKEN"),
            base_url="https://api-inference.huggingface.co/models/Qwen/Qwen2.5-72B-Instruct/v1",
        )

    def ask_question(self, text: str, *, max_chars: int = 200) -> str:
        prompt_template = PromptTemplate(
            input_variables=["text"],
            template="""
            You are an expert in the Brazilian accounting system, legislation and a technology specialist, a
            personal assistant for a company called Accord Contabilidade. That said, you should use your knowledge
            to answer the following question: {text} Answer me in portuguese.
            """.replace(
                "@", ""
            ),
        )

        prompt = prompt_template.format(text=text)

        response = self.llm.invoke(prompt)

        return response
