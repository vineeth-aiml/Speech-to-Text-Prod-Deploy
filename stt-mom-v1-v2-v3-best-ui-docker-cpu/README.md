# Offline Speech-to-Text + MoM — V1 / V2 / V3 (CPU) + Docker

A **CPU-only, offline-first** meeting assistant with:
- **Live streaming STT** (WebSocket) -> realtime transcript
- **MoM generation**
  - **V1**: rule-based (always works offline)
  - **V2**: offline local LLM via **Ollama** (better quality) (default)
- **V3**: collaborative rooms (multi-tab/users), exports, feature flags, docker deployment

**Languages:** English + Indian languages (Whisper multilingual).  
**MoM language:** same as detected/selected language.

---

## Quick Start (Docker)

### 1) Start everything
```bash
docker compose up --build
```

- Frontend: http://localhost:5173  
- Backend: http://localhost:8000/docs

### 2) V2 MoM (Ollama optional)
Install Ollama and run:
```bash
ollama run qwen2.5:3b-instruct
```
If Ollama is not running, system auto-falls back to V1.

---

## Run without Docker (Windows CPU)

### Backend
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

---

## V3 collaboration
Open UI in 2 tabs, set same Room ID, click Start in one tab -> transcript broadcasts to both.

