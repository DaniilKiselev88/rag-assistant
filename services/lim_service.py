from langchain_community.llms import Ollama

MODEL_NAME = "llama3.2"


def get_llm():
    return Ollama(
        model=MODEL_NAME,
        temperature=0
    )