# ----------------------------
# 1. Import FastAPI framework
# ----------------------------
from fastapi import FastAPI  # creates API server
from pydantic import BaseModel  # defines request body structure

# ----------------------------
# 2. LangChain imports
# ----------------------------
from langchain_groq import ChatGroq  # Groq LLM (Llama models)

from langchain_community.tools import (
    ArxivQueryRun,  # tool for research papers
    WikipediaQueryRun,  # tool for Wikipedia search
    DuckDuckGoSearchRun  # tool for web search
)

from langchain_community.utilities import (
    WikipediaAPIWrapper,  # backend for Wikipedia tool
    ArxivAPIWrapper       # backend for Arxiv tool
)

from langchain_classic.agents import initialize_agent, AgentType  # agent system

# ----------------------------
# 3. Environment loading
# ----------------------------
import os  # access environment variables
from dotenv import load_dotenv  # load .env file

load_dotenv()  # load API keys from .env file

# ----------------------------
# 4. Get API key
# ----------------------------
groq_api_key = os.getenv("GROQ_API_KEY")

# ----------------------------
# 5. Create FastAPI app
# ----------------------------
app = FastAPI(title="LangChain Search Agent API")

# ----------------------------
# 6. Define request format
# ----------------------------
class QueryRequest(BaseModel):
    question: str  # user question sent to API

# ----------------------------
# 7. Setup tools
# ----------------------------

# Arxiv tool setup (scientific papers search)
arxiv_wrapper = ArxivAPIWrapper(
    top_k_results=1,  # return only 1 result
    doc_content_chars_max=200  # limit response size
)
arxiv = ArxivQueryRun(api_wrapper=arxiv_wrapper)

# Wikipedia tool setup
wiki_wrapper = WikipediaAPIWrapper(
    top_k_results=1,
    doc_content_chars_max=200
)
wiki = WikipediaQueryRun(api_wrapper=wiki_wrapper)

# Web search tool
search = DuckDuckGoSearchRun(name="Search")

# Combine all tools into one list
tools = [search, arxiv, wiki]

# ----------------------------
# 8. Create LLM (brain of agent)
# ----------------------------
llm = ChatGroq(
    groq_api_key=groq_api_key,  # authentication key
    model_name="meta-llama/llama-4-scout-17b-16e-instruct",  # model used
    streaming=False  # FastAPI usually uses non-streaming
)

# ----------------------------
# 9. Create agent
# ----------------------------
search_agent = initialize_agent(
    tools=tools,  # tools available to agent
    llm=llm,  # LLM brain
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,  # reasoning strategy
    handle_parsing_errors=True  # avoids crashes when tool output is messy
)

# ----------------------------
# 10. API endpoint
# ----------------------------
@app.post("/chat")  # POST endpoint
def chat(request: QueryRequest):
    """
    This function:
    1. receives user question
    2. sends it to the agent
    3. returns response
    """

    # Run agent with user input
    response = search_agent.run(request.question)

    # Return structured JSON response
    return {
        "question": request.question,
        "answer": response
    }