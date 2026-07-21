# Vyronix AI

**Perceive. Reason. Retrieve. Respond.**

Vyronix AI is a multimodal AI assistant that combines Computer Vision, Retrieval-Augmented Generation (RAG), Agentic AI, Memory and Voice Interaction to provide context-aware assistance in real time.

## Architecture

```text
                   User
                     │
      ┌──────────────┼──────────────┐
      │              │              │
   Voice         Text Input     Live Camera
      │              │              │
      └──────────────┼──────────────┘
                     │
             HTML • CSS • JavaScript
                     │
                  FastAPI
                     │
             LangGraph AI Agent
                     │
      ┌──────────────┼──────────────┐
      │              │              │
 Vision Tool     RAG Tool     Memory Tool
(OpenCV, YOLO,   (FAISS,      Chat + Scene
 EasyOCR)        PDFs)        Memory
      │              │              │
      └──────────────┼──────────────┘
                     │
               Prompt Builder
                     │
                 Groq LLM
                     │
            Text & Voice Response
```

---

## Tech Stack
- Language: Python
- Frontend: HTML, CSS, JavaScript
- Backend: FastAPI
- AI Agent: LangGraph
- LLM: Groq
- Computer Vision: OpenCV, YOLOv8, EasyOCR
- RAG: LangChain, FAISS, Sentence Transformers
- Speech: Faster Whisper, Edge-TTS

---

## Project Structure

```text
Vyronix_AI/
│
├── frontend/
├── backend/
├── vision/
├── rag/
├── agent/
├── memory/
├── speech/
├── uploads/
├── vectorstore/
│
├── .env
├── pyproject.toml
├── uv.lock
└── README.md
```
## Installation

```bash
git clone <repository-url>
cd Vyronix_AI
uv sync
source .venv/bin/activate
```
## Environment Variables

```env
GROQ_API_KEY=your_api_key
HF_TOKEN=your_huggingface_token
```
## Run

```bash
uv run uvicorn backend.main:app --reload
```

## Current Development Roadmap

- [ ] Frontend Interface
- [ ] FastAPI Backend
- [ ] Computer Vision
- [ ] RAG Pipeline
- [ ] AI Agent
- [ ] Voice Assistant
- [ ] Complete Integration

---

**Author:** Mayank Choubey