from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

import shutil
import os
import base64
import threading
import time

from rag.pipeline import ingest, search_rag
from rag.embedder import get_embedding_model
from rag.vector_store import load_vector_store

from agent.agent import ask
from agent.tools import scene_memory  # same singleton scene_tool() reads from

from vision.camera import Camera
from vision.yolo_detector import ObjectDetector
from vision.ocr import OCRReader

from speech.stt import SpeechToText
from speech.tts import TextToSpeech


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
# Vector store - kept in memory, reloaded whenever new content is ingested
# -------------------------------

embedding_model = get_embedding_model()
db = None


def _try_load_existing_db():
    global db
    try:
        db = load_vector_store(embedding_model)
        print("Loaded existing vector store from disk.")
    except Exception:
        db = None
        print("No existing vector store found yet - upload a file or website first.")


_try_load_existing_db()

# -------------------------------
# Speech components - loaded once at startup (model load is slow)
# -------------------------------

speech_to_text = SpeechToText()
text_to_speech = TextToSpeech()

# -------------------------------
# Vision: continuous background loop
# -------------------------------

object_detector = ObjectDetector()
ocr_reader = OCRReader()

vision_camera = None
vision_thread_running = False

# How often to run each step (seconds). OCR is slower than detection,
# so we run it less frequently to keep the loop responsive.
DETECTION_INTERVAL = 1.0
OCR_INTERVAL = 4.0


def _continuous_vision_loop():
    global vision_camera

    vision_camera = Camera()
    last_ocr_time = 0.0

    print("Vision loop started - camera is now always on.")

    while vision_thread_running:

        frame = vision_camera.get_frame()

        if frame is not None:

            # Object detection - every loop tick
            objects = object_detector.detect(frame)
            scene_memory.update_objects(objects)

            # OCR - only every OCR_INTERVAL seconds (it's the slow step)
            now = time.time()
            if now - last_ocr_time >= OCR_INTERVAL:
                text = ocr_reader.extract_text(frame)
                scene_memory.update_text(text)
                last_ocr_time = now

        time.sleep(DETECTION_INTERVAL)

    vision_camera.release()
    print("Vision loop stopped - camera released.")


@app.on_event("startup")
def start_vision_loop():
    global vision_thread_running
    vision_thread_running = True
    thread = threading.Thread(target=_continuous_vision_loop, daemon=True)
    thread.start()


@app.on_event("shutdown")
def stop_vision_loop():
    global vision_thread_running
    vision_thread_running = False


# -------------------------------
# Request Models
# -------------------------------

class ChatRequest(BaseModel):
    question: str


class WebsiteRequest(BaseModel):
    url: str


class TextRequest(BaseModel):
    text: str


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

    global db
    db = ingest(save_path)

    return {
        "status": "success",
        "file": file.filename
    }


# -------------------------------
# Upload Website
# -------------------------------

@app.post("/website")
def upload_website(request: WebsiteRequest):

    global db
    db = ingest(request.url)

    return {
        "status": "success",
        "url": request.url
    }


# -------------------------------
# Ask Question (text chat)
# -------------------------------

@app.post("/chat")
def chat(request: ChatRequest):

    if db is None:
        return {
            "question": request.question,
            "answer": "No documents ingested yet. Please upload a file or add a website first."
        }

    answer = ask(request.question, db)

    return {
        "question": request.question,
        "answer": answer
    }


# -------------------------------
# Retrieve only (Debug API)
# -------------------------------

@app.post("/retrieve")
def retrieve(request: ChatRequest):

    if db is None:
        return {"results": []}

    docs = search_rag(request.question, db)

    return {
        "results": [
            doc.page_content
            for doc in docs
        ]
    }


# -------------------------------
# Vision: get the latest scene (no capture triggered here -
# the background loop is already continuously updating it)
# -------------------------------

@app.get("/vision/live")
def vision_live():

    scene = scene_memory.get_scene()

    return {
        "objects": scene["objects"],
        "text": scene["text"]
    }


# -------------------------------
# Speech: Transcribe only (Debug API)
# -------------------------------

@app.post("/speech/transcribe")
async def transcribe(file: UploadFile = File(...)):

    temp_path = os.path.join(UPLOAD_FOLDER, f"stt_{file.filename}")

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = speech_to_text.transcribe(temp_path)

    os.remove(temp_path)

    return {"text": text}


# -------------------------------
# Speech: Synthesize only (Debug API) - returns an mp3 file
# -------------------------------

@app.post("/speech/synthesize")
async def synthesize(request: TextRequest):

    output_path = os.path.join(UPLOAD_FOLDER, "synthesized.mp3")

    await text_to_speech.speak(request.text, output_path)

    return FileResponse(output_path, media_type="audio/mpeg")


# -------------------------------
# Voice Ask (full loop): audio in -> STT -> agent -> TTS -> audio out
# -------------------------------

@app.post("/voice/ask")
async def voice_ask(file: UploadFile = File(...)):

    if db is None:
        return {"error": "No documents ingested yet. Please upload a file or add a website first."}

    temp_path = os.path.join(UPLOAD_FOLDER, f"voice_{file.filename}")

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    question = speech_to_text.transcribe(temp_path)
    os.remove(temp_path)

    if not question:
        return {"error": "Could not understand audio. Please try again."}

    answer = ask(question, db)

    audio_path = os.path.join(UPLOAD_FOLDER, "voice_response.mp3")
    await text_to_speech.speak(answer, audio_path)

    with open(audio_path, "rb") as f:
        audio_b64 = base64.b64encode(f.read()).decode("utf-8")

    return {
        "question": question,
        "answer": answer,
        "audio_base64": audio_b64
    }