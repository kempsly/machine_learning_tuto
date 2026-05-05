import os
from flask import Flask, request, render_template
from dotenv import load_dotenv

from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load env variables
load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY", "")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY", "")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "simple_ollama_flask_app"


app = Flask(__name__)

# Prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Please respond to the question asked"),
    ("user", "Question: {question}")
])

# LLM
llm = Ollama(model="llama2")

# Chain
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

@app.route("/", methods=["GET", "POST"])
def home():
    answer=None
    
    if request.method =="POST":
        question = request.form.get("question")
        
        if question:
            answer=chain.invoke({"question": question})
            
    return render_template("index.html", answer=answer)

if __name__=="__main__":
    app.run(debug=True)