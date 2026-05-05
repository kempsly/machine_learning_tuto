import os
from dotenv import load_dotenv

from fastapi import FastAPI
from pydantic import BaseModel

from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load env
load_dotenv()

os.environ["LANGCHAIN_PROJECT"] = "simple_ollama_fastapi"
os.environ["LANGCHAIN_TRACING_V2"] = "true"

# FastAPI app
app = FastAPI(title="LangChain Ollama API")

# Request schema
class QuestionRequest(BaseModel):
    question: str

# Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("user", "Question: {question}")
])

# LLM
llm = Ollama(model="llama2")

# Chain
output_parser = StrOutputParser()
chain = prompt | llm | output_parser


@app.get("/")
def home():
    return {"message": "LangChain + Ollama API is running 🚀"}


@app.post("/chat")
def chat(req: QuestionRequest):
    response = chain.invoke({"question": req.question})
    return {"answer": response}