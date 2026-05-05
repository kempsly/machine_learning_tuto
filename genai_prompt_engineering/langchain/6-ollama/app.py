import os
from dotenv import load_dotenv
from langchain_community.llms import Ollama
import streamlit as st 
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


load_dotenv()

os.environ['OPENAI_API_KEY']=os.getenv("OPENAI_API_KEY")
## Langsmith Tracking
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]="true"
# os.environ["LANGCHAIN_PROJECT"]=os.getenv("LANGCHAIN_PROJECT")

app_name = "simple_ollama_app"
os.environ["LANGCHAIN_PROJECT"] = app_name



# Define our prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Please respond to the question asked"),
        ("user", "Question:{question}")
    ]
)

# Streamlit framework:
st.title("Langchain Demo With LLAMA2")
input_text = st.text_input("what question you have in mind")

### Ollama llama2
llm=Ollama(model="llama2")
# llm=Ollama()
output_parser = StrOutputParser()
chain = prompt|llm|output_parser

if input_text:
    st.write(chain.invoke({"question": input_text}))