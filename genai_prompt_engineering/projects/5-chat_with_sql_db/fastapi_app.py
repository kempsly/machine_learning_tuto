# ----------------------------
# 1. FastAPI & request schema
# ----------------------------
from fastapi import FastAPI  # create API server
from pydantic import BaseModel  # define request body

# ----------------------------
# 2. LangChain imports
# ----------------------------
from langchain_classic.agents import create_sql_agent  # SQL agent creator
from langchain_classic.sql_database import SQLDatabase  # DB wrapper
from langchain_classic.agents.agent_types import AgentType  # agent type
from langchain_classic.agents.agent_toolkits import SQLDatabaseToolkit  # tools for SQL agent

# ----------------------------
# 3. Database + utilities
# ----------------------------
from sqlalchemy import create_engine  # DB engine
from pathlib import Path  # file path handling
import sqlite3  # SQLite connector

# ----------------------------
# 4. LLM (Groq)
# ----------------------------
from langchain_groq import ChatGroq

# ----------------------------
# 5. Environment variables
# ----------------------------
import os
from dotenv import load_dotenv

load_dotenv()  # load .env file

groq_api_key = os.getenv("GROQ_API_KEY")  # get API key

# ----------------------------
# 6. Create FastAPI app
# ----------------------------
app = FastAPI(title="SQL Agent API")

# ----------------------------
# 7. Request schema
# ----------------------------
class QueryRequest(BaseModel):
    question: str  # user question
    db_type: str = "sqlite"  # default DB type
    mysql_host: str | None = None
    mysql_user: str | None = None
    mysql_password: str | None = None
    mysql_db: str | None = None

# ----------------------------
# 8. Initialize LLM
# ----------------------------
llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="meta-llama/llama-4-scout-17b-16e-instruct",
    streaming=False  # no streaming in API
)

# ----------------------------
# 9. Database configuration
# ----------------------------
def configure_db(db_type, mysql_host=None, mysql_user=None, mysql_password=None, mysql_db=None):

    # SQLite case
    if db_type == "sqlite":
        dbfilepath = (Path(__file__).parent / "student.db").absolute()

        # read-only connection
        creator = lambda: sqlite3.connect(f"file:{dbfilepath}?mode=ro", uri=True)

        # wrap DB for LangChain
        return SQLDatabase(create_engine("sqlite:///", creator=creator))

    # MySQL case
    elif db_type == "mysql":
        if not (mysql_host and mysql_user and mysql_password and mysql_db):
            raise ValueError("Missing MySQL credentials")

        return SQLDatabase(
            create_engine(
                f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"
            )
        )

# ----------------------------
# 10. API endpoint
# ----------------------------
@app.post("/chat")
def chat(request: QueryRequest):
    """
    This endpoint:
    1. connects to DB
    2. creates SQL agent
    3. runs query
    4. returns response
    """

    # ----------------------------
    # Create DB connection
    # ----------------------------
    db = configure_db(
        request.db_type,
        request.mysql_host,
        request.mysql_user,
        request.mysql_password,
        request.mysql_db
    )

    # ----------------------------
    # Create toolkit
    # ----------------------------
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)

    # ----------------------------
    # Create SQL agent
    # ----------------------------
    agent = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
    )

    # ----------------------------
    # Run query
    # ----------------------------
    response = agent.run(request.question)

    # ----------------------------
    # Return result
    # ----------------------------
    return {
        "question": request.question,
        "answer": response
    }