# -------------------------
# Core imports
# -------------------------
from fastapi import FastAPI  # FastAPI framework to create APIs
from pydantic import BaseModel  # For request validation
import os  # For environment variables
from dotenv import load_dotenv  # Load .env file

# -------------------------
# LangChain / RAG imports
# -------------------------
from langchain_groq import ChatGroq  # LLM via Groq (Llama3)
from langchain_openai import OpenAIEmbeddings  # Embedding model
from langchain.text_splitter import RecursiveCharacterTextSplitter  # Split documents into chunks
from langchain.chains.combine_documents import create_stuff_documents_chain  # Combine retrieved docs
from langchain_core.prompts import ChatPromptTemplate  # Prompt template
from langchain.chains import create_retrieval_chain  # RAG chain
from langchain_community.vectorstores import FAISS  # Vector database
from langchain_community.document_loaders import PyPDFDirectoryLoader  # Load PDFs

# -------------------------
# Load environment variables
# -------------------------
load_dotenv()  # Load variables from .env file

# Set API keys (used internally by LangChain)
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")
os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")

# -------------------------
# Initialize FastAPI app
# -------------------------
app = FastAPI(
    title="RAG API with Groq + FAISS",
    version="1.0"
)

# -------------------------
# Initialize LLM (Groq)
# -------------------------
groq_api_key = os.getenv("GROQ_API_KEY")  # Get Groq API key

llm = ChatGroq(
    groq_api_key=groq_api_key,  # Pass API key
    model_name="Llama3-8b-8192"  # Model used
)

# -------------------------
# Prompt template
# -------------------------
prompt = ChatPromptTemplate.from_template(
    """
    Answer the questions based on the provided context only.
    Please provide the most accurate response based on the question.

    <context>
    {context}
    </context>

    Question: {input}
    """
)

# -------------------------
# Global variable (replacement for session_state)
# -------------------------
vector_store = None  # Will hold FAISS index

# -------------------------
# Function to create embeddings (like your Streamlit function)
# -------------------------
def create_vector_embedding():
    global vector_store  # Use global variable

    if vector_store is None:  # Only create once (like session_state check)

        embeddings = OpenAIEmbeddings()  # Initialize embedding model

        loader = PyPDFDirectoryLoader("research_papers")  # Load PDFs from folder

        docs = loader.load()  # Read all documents

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,  # Size of each chunk
            chunk_overlap=200  # Overlap between chunks
        )

        final_documents = text_splitter.split_documents(docs[:50])  
        # Split first 50 docs into chunks

        vector_store = FAISS.from_documents(
            final_documents,  # Document chunks
            embeddings  # Embedding model
        )
        # Create FAISS vector index

    return "Vector DB ready"


# -------------------------
# Request schema
# -------------------------
class QueryRequest(BaseModel):
    question: str  # User question


# -------------------------
# Endpoint to initialize embeddings
# -------------------------
@app.post("/embed")
def embed_documents():
    message = create_vector_embedding()  # Build vector DB
    return {"status": message}


# -------------------------
# Endpoint for querying (RAG)
# -------------------------
@app.post("/ask")
def ask_question(request: QueryRequest):
    global vector_store  # Access global vector DB

    if vector_store is None:
        return {"error": "Vector DB not initialized. Call /embed first."}

    # Create document chain (LLM + prompt)
    document_chain = create_stuff_documents_chain(
        llm,  # LLM
        prompt  # Prompt template
    )

    # Convert vector store to retriever
    retriever = vector_store.as_retriever()

    # Create full RAG pipeline
    retrieval_chain = create_retrieval_chain(
        retriever,  # Retrieves relevant docs
        document_chain  # Generates answer
    )

    import time
    start = time.process_time()  # Start timer

    response = retrieval_chain.invoke({
        "input": request.question  # Pass user question
    })

    end = time.process_time()  # End timer

    return {
        "answer": response["answer"],  # Final answer
        "response_time": end - start,  # Time taken
        "documents": [doc.page_content for doc in response["context"]]  
        # Return retrieved documents (like Streamlit expander)
    }


# -------------------------
# Run server
# -------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)