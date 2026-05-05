from fastapi import FastAPI 
from langchain_core.prompts import ChatPromptTemplate 
from langchain_core.output_parsers import StrOutputParser 
from langchain_groq import ChatGroq 
import os 
from dotenv import load_dotenv
from langserve import add_routes 
from langchain_core.messages import HumanMessage, SystemMessage


load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
model = ChatGroq(
    model="meta-llama/llama-4-scout-17b-16e-instruct",  # active model
    groq_api_key=groq_api_key
)


###Prompt templates
system_template="Translate the following into {language}:"
prompt_template = ChatPromptTemplate.from_messages(
    [("system", system_template), ("user","{text}")]
)

parser = StrOutputParser()

# Create chain
chain = prompt_template|model|parser

####App definition
app = FastAPI(title="Langchain Server",
              version="1.0",
              description="A simple API Server using Langchain runnable interfaces")

####Adding chain routes
# It automatically creates FastAPI endpoints for your chain
# “Take this LangChain pipeline and expose it as a web API 
# without me writing endpoints manually.”
add_routes(
    app,
    chain,
    path="/chain"
    
)

if __name__=="__main__":
    import uvicorn 
    uvicorn.run(app, host="localhost", port=8000)