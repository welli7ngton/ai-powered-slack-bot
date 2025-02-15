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
            api_key=getenv("HF_TOKEN", "None"),
            base_url="https://api-inference.huggingface.co/models/Qwen/Qwen2.5-72B-Instruct/v1",
        )

    def ask_question(self, text: str, *, max_chars: int = 800) -> str:
        prompt_template = PromptTemplate(
            input_variables=["text", "max_chars"],
            template="""
            You are an expert in technology. You should use your knowledge to answer the following question:
            {text}. Answer me in Portuguese and do not exceed {max_chars} characters.
            """,
        )

        prompt = prompt_template.format(text=text, max_chars=max_chars)

        response = self.llm.invoke(prompt)

        # Ensure the response does not exceed max_chars
        return response[:max_chars]
