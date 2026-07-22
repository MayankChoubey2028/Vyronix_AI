from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import shutil
import os

from rag.pipeline import ingest, query
from agent.agent import ask

app = FastAPI(title="Vyronix AI")

# -------------------------------
# CORS
# -------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# -------------------------------
# Request Models
# -------------------------------

class ChatRequest(BaseModel):
    question: str


class WebsiteRequest(BaseModel):
    url: str


# -------------------------------
# Home
# -------------------------------

@app.get("/")
def home():

    return {
        "message": "Vyronix AI Backend Running"
    }


# -------------------------------
# Upload PDF / DOCX / TXT
# -------------------------------

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    save_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    ingest(save_path)

    return {
        "status": "success",
        "file": file.filename
    }


# -------------------------------
# Upload Website
# -------------------------------

@app.post("/website")
def upload_website(request: WebsiteRequest):

    ingest(request.url)

    return {
        "status": "success",
        "url": request.url
    }


# -------------------------------
# Ask Question
# -------------------------------

@app.post("/chat")
def chat(request: ChatRequest):

    answer = ask(request.question)

    return {
        "question": request.question,
        "answer": answer
    }


# -------------------------------
# Retrieve only (Debug API)
# -------------------------------

@app.post("/retrieve")
def retrieve(request: ChatRequest):

    docs = query(request.question)

    return {
        "results": [
            doc.page_content
            for doc in docs
        ]
    }