# -------------------------
# Core FastAPI imports
# -------------------------
from fastapi import FastAPI, UploadFile, File  # API + file upload
from pydantic import BaseModel  # Request validation
from typing import List  # For handling multiple files
import os
from dotenv import load_dotenv

# -------------------------
# LangChain / RAG imports
# -------------------------
from langchain_classic.chains import create_history_aware_retriever, create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma  # Vector DB
from langchain_community.chat_message_histories import ChatMessageHistory  # Chat memory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq  # LLM (Groq)
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_huggingface import HuggingFaceEmbeddings  # Embeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

# -------------------------
# Load environment variables
# -------------------------
load_dotenv()

os.environ['HF_TOKEN'] = os.getenv("HF_TOKEN")  # HuggingFace token

# -------------------------
# Initialize FastAPI app
# -------------------------
app = FastAPI(
    title="Conversational RAG API",
    version="1.0"
)

# -------------------------
# Global objects (replace Streamlit session_state)
# -------------------------
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")  # Embedding model
vector_store = None  # Will store Chroma DB
retriever = None  # Will store retriever
store = {}  # Chat history storage per session_id

# -------------------------
# Request schema for chat
# -------------------------
class ChatRequest(BaseModel):
    question: str  # User question
    session_id: str = "default_session"  # Conversation session
    api_key: str  # Groq API key


# -------------------------
# Upload + process PDFs
# -------------------------
@app.post("/upload")
async def upload_pdfs(files: List[UploadFile] = File(...)):
    global vector_store, retriever

    documents = []  # Store all loaded documents

    for file in files:
        temp_path = f"./temp_{file.filename}"  # Temporary file path

        # Save uploaded file locally
        with open(temp_path, "wb") as f:
            f.write(await file.read())

        # Load PDF content
        loader = PyPDFLoader(temp_path)
        docs = loader.load()

        documents.extend(docs)  # Add to list

    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=5000,
        chunk_overlap=500
    )

    splits = text_splitter.split_documents(documents)

    # Create vector database (Chroma)
    vector_store = Chroma.from_documents(
        documents=splits,
        embedding=embeddings
    )

    # Create retriever
    retriever = vector_store.as_retriever()

    return {"status": "Documents processed and vector DB ready"}


# -------------------------
# Helper: get session history
# -------------------------
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    # If session does not exist → create it
    if session_id not in store:
        store[session_id] = ChatMessageHistory()

    return store[session_id]


# -------------------------
# Chat endpoint (RAG + memory)
# -------------------------
@app.post("/chat")
def chat(request: ChatRequest):
    global retriever

    if retriever is None:
        return {"error": "Upload PDFs first via /upload"}

    # Initialize LLM with user API key
    llm = ChatGroq(
        groq_api_key=request.api_key,
        model_name="meta-llama/llama-4-scout-17b-16e-instruct"
    )

    # -------------------------
    # Step 1: Reformulate question using chat history
    # -------------------------
    contextual_q_system_prompt = (
        "Given a chat history and the latest user question "
        "which might reference context in the chat history, "
        "formulate a standalone question. Do NOT answer it."
    )

    contextual_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextual_q_system_prompt),
            MessagesPlaceholder("chat_history"),  # Inject history
            ("human", "{input}")
        ]
    )

    # Create history-aware retriever
    history_aware_retriever = create_history_aware_retriever(
        llm,
        retriever,
        contextual_q_prompt
    )

    # -------------------------
    # Step 2: Answer generation
    # -------------------------
    system_prompt = (
        "You are an assistant for question-answering tasks. "
        "Use retrieved context to answer. "
        "If unknown, say you don't know. "
        "Max 3 sentences.\n\n{context}"
    )

    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder("chat_history"),  # Include history again
            ("human", "{input}")
        ]
    )

    # Combine docs + LLM
    question_answer_chain = create_stuff_documents_chain(
        llm,
        qa_prompt
    )

    # Create full RAG pipeline
    rag_chain = create_retrieval_chain(
        history_aware_retriever,
        question_answer_chain
    )

    # -------------------------
    # Step 3: Add memory (chat history)
    # -------------------------
    conversational_rag_chain = RunnableWithMessageHistory(
        rag_chain,
        get_session_history,  # function to retrieve history
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer"
    )

    # Execute RAG chain
    response = conversational_rag_chain.invoke(
        {"input": request.question},
        config={
            "configurable": {"session_id": request.session_id}
        }
    )

    # Return answer + history
    return {
        "answer": response["answer"],
        "chat_history": [msg.content for msg in get_session_history(request.session_id).messages]
    }


# -------------------------
# Run server
# -------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)