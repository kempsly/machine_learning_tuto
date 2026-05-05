from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

# LangSmith (optional)
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Basic Q&A Chatbot With OpenAI"

app = FastAPI(
    title="Q&A Chatbot API",
    version="1.0",
    description="FastAPI version of your Streamlit chatbot"
)

# -------------------------
# Prompt
# -------------------------
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Please respond to the user query"),
        ("user", "Question:{question}")
    ]
)

# -------------------------
# Request schema
# -------------------------
class ChatRequest(BaseModel):
    question: str
    api_key: str
    model: str = "gpt-4o"
    temperature: float = 0.7
    max_tokens: int = 150


# -------------------------
# Core function
# -------------------------
def generate_response(data: ChatRequest):
    if not data.api_key:
        raise HTTPException(status_code=400, detail="API key is required")

    os.environ["OPENAI_API_KEY"] = data.api_key

    llm = ChatOpenAI(
        model=data.model,
        temperature=data.temperature,
        max_tokens=data.max_tokens
    )

    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser

    answer = chain.invoke({"question": data.question})
    return answer


# -------------------------
# Endpoint
# -------------------------
@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    response = generate_response(request)
    return {"response": response}


# -------------------------
# Run
# -------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)