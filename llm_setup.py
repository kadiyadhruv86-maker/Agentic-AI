"""Minimal first check: verify the local ChatOllama call before running RAG or tools."""
from langchain_ollama import ChatOllama
from config import settings

def get_chat_model():
    return ChatOllama(
        model=settings.ollama_model,
        base_url=settings.ollama_base_url,
        temperature=0.1,
    )

if __name__ == "__main__":
    llm = get_chat_model()
    response = llm.invoke("Reply with exactly: ChatOllama is working.")
    print(response.content)
