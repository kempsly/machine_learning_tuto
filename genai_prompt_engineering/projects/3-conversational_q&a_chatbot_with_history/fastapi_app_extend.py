# -------------------------
# FastAPI + async support
# -------------------------
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List
import os
from dotenv import load_dotenv
import asyncio

# -------------------------
# LangChain imports
# -------------------------
from langchain_classic.chains import create_history_aware_retriever, create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

# -------------------------
# Load environment variables
# -------------------------
load_dotenv()
os.environ['HF_TOKEN'] = os.getenv("HF_TOKEN")

# -------------------------
# App initialization
# -------------------------
app = FastAPI(title="Advanced Conversational RAG API")

# -------------------------
# Global resources
# -------------------------
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

vector_store = None        # Stores vector DB
retriever = None           # Retriever
chat_store = {}            # Stores chat history per session

# -------------------------
# Request schema
# -------------------------
class ChatRequest(BaseModel):
    question: str
    session_id: str
    api_key: str


# -------------------------
# Upload PDFs (async)
# -------------------------
@app.post("/upload")
async def upload(files: List[UploadFile] = File(...)):
    global vector_store, retriever

    documents = []

    for file in files:
        temp_path = f"./temp_{file.filename}"

        # Save file asynchronously
        with open(temp_path, "wb") as f:
            f.write(await file.read())

        # Load PDF content
        loader = PyPDFLoader(temp_path)
        docs = loader.load()
        documents.extend(docs)

    # Split documents into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=5000,
        chunk_overlap=500
    )
    splits = splitter.split_documents(documents)

    # Create vector DB (Chroma)
    vector_store = Chroma.from_documents(splits, embeddings)

    # Create retriever
    retriever = vector_store.as_retriever()

    return {"status": "Vector DB ready"}


# -------------------------
# Chat history manager
# -------------------------
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in chat_store:
        chat_store[session_id] = ChatMessageHistory()
    return chat_store[session_id]


# -------------------------
# Build RAG chain (reusable)
# -------------------------
def build_rag_chain(llm):

    # -------- Step 1: Contextual question reformulation --------
    contextual_prompt = ChatPromptTemplate.from_messages([
        ("system", "Rephrase the question based on chat history. Do NOT answer."),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}")
    ])

    history_retriever = create_history_aware_retriever(
        llm,
        retriever,
        contextual_prompt
    )

    # -------- Step 2: Answer generation --------
    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", "Answer using context. Max 3 sentences.\n\n{context}"),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}")
    ])

    qa_chain = create_stuff_documents_chain(llm, qa_prompt)

    rag_chain = create_retrieval_chain(history_retriever, qa_chain)

    # -------- Step 3: Add memory --------
    conversational_chain = RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer"
    )

    return conversational_chain


# -------------------------
# Streaming generator
# -------------------------
async def stream_response(chain, question, session_id):
    """
    Streams response token-by-token
    """

    # Run in thread (LangChain is sync)
    loop = asyncio.get_event_loop()

    response = await loop.run_in_executor(
        None,
        lambda: chain.invoke(
            {"input": question},
            config={"configurable": {"session_id": session_id}}
        )
    )

    # Simulate streaming (since Groq wrapper may not stream directly)
    for word in response["answer"].split():
        yield word + " "
        await asyncio.sleep(0.02)  # small delay for streaming effect


# -------------------------
# Chat endpoint (streaming)
# -------------------------
@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    global retriever

    if retriever is None:
        return {"error": "Upload documents first"}

    # Initialize LLM
    llm = ChatGroq(
        groq_api_key=request.api_key,
        model_name="meta-llama/llama-4-scout-17b-16e-instruct"
    )

    # Build RAG chain
    chain = build_rag_chain(llm)

    # Return streaming response
    return StreamingResponse(
        stream_response(chain, request.question, request.session_id),
        media_type="text/plain"
    )


# -------------------------
# Standard chat endpoint
# -------------------------
@app.post("/chat")
async def chat(request: ChatRequest):
    global retriever

    if retriever is None:
        return {"error": "Upload documents first"}

    llm = ChatGroq(
        groq_api_key=request.api_key,
        model_name="meta-llama/llama-4-scout-17b-16e-instruct"
    )

    chain = build_rag_chain(llm)

    response = chain.invoke(
        {"input": request.question},
        config={"configurable": {"session_id": request.session_id}}
    )

    return {
        "answer": response["answer"],
        "history": [
            msg.content for msg in get_session_history(request.session_id).messages
        ]
    }


# -------------------------
# Health check endpoint
# -------------------------
@app.get("/")
def health():
    return {"status": "API running"}