from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import json
import os
from pathlib import Path
from chatbot import match_question

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,  # FIXED: must be False when allow_origins=["*"]
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get the base directory (backend folder)
BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"
DATA_DIR = BASE_DIR / "data"

# Mount static files (frontend folder) - only if it exists
if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

# Data file paths
FAQ_FILE = str(DATA_DIR / "faq.json")
QUERIES_FILE = str(DATA_DIR / "new_queries.json")

# Ensure data directory exists
DATA_DIR.mkdir(exist_ok=True)

# Initialize files if they don't exist
if not os.path.exists(FAQ_FILE):
    with open(FAQ_FILE, "w") as f:
        json.dump([
            {"id": 1, "question": "What are the college timings?", "answer": "College timings are 9:00 AM to 4:00 PM, Monday to Friday."},
            {"id": 2, "question": "How do I apply for admission?", "answer": "You can apply online through our website or visit the admissions office."},
            {"id": 3, "question": "What courses are offered?", "answer": "We offer B.Tech, M.Tech, MBA, and various undergraduate programs."}
        ], f, indent=2)

if not os.path.exists(QUERIES_FILE):
    with open(QUERIES_FILE, "w") as f:
        json.dump([], f, indent=2)

# Models
class ChatRequest(BaseModel):
    message: str

class FAQRequest(BaseModel):
    question: str
    answer: str

class FAQUpdate(BaseModel):
    id: int
    question: str
    answer: str

class LoginRequest(BaseModel):
    username: str
    password: str

# Helper functions
def load_json(filepath):
    try:
        with open(filepath, "r") as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_json(filepath, data):
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

# Frontend Routes
@app.head("/")  # FIXED: handle Render health check HEAD request
def head_index():
    return Response(status_code=200)

@app.get("/")
def serve_index():
    index_path = FRONTEND_DIR / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=404, detail=f"Frontend file not found at {index_path}")
    return FileResponse(str(index_path))

@app.get("/dashboard")
def serve_dashboard():
    dashboard_path = FRONTEND_DIR / "dashboard.html"
    if not dashboard_path.exists():
        raise HTTPException(status_code=404, detail=f"Dashboard file not found at {dashboard_path}")
    return FileResponse(str(dashboard_path))

@app.get("/index.html")
def serve_index_html():
    index_path = FRONTEND_DIR / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=404, detail=f"Frontend file not found at {index_path}")
    return FileResponse(str(index_path))

@app.get("/dashboard.html")
def serve_dashboard_html():
    dashboard_path = FRONTEND_DIR / "dashboard.html"
    if not dashboard_path.exists():
        raise HTTPException(status_code=404, detail=f"Dashboard file not found at {dashboard_path}")
    return FileResponse(str(dashboard_path))

# API Routes
@app.get("/api")
def root():
    return {"message": "AskBot API is running"}

@app.post("/chat")
def chat(request: ChatRequest):
    faqs = load_json(FAQ_FILE)
    result = match_question(request.message, faqs)

    if result:
        return {"answer": result["answer"], "matched": True}
    else:
        queries = load_json(QUERIES_FILE)
        query_id = max([q.get("id", 0) for q in queries], default=0) + 1
        queries.append({"id": query_id, "question": request.message})
        save_json(QUERIES_FILE, queries)
        return {"answer": "I'm sorry, I don't have an answer for that. Your question has been logged for review.", "matched": False}

@app.post("/admin/login")
def admin_login(request: LoginRequest):
    admin_user = os.getenv("ADMIN_USER", "admin")
    admin_pass = os.getenv("ADMIN_PASS", "1234")
    if request.username == admin_user and request.password == admin_pass:
        return {"success": True, "message": "Login successful"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/get-faqs")
def get_faqs():
    return load_json(FAQ_FILE)

@app.post("/add-faq")
def add_faq(request: FAQRequest):
    faqs = load_json(FAQ_FILE)
    new_id = max([faq.get("id", 0) for faq in faqs], default=0) + 1
    new_faq = {"id": new_id, "question": request.question, "answer": request.answer}
    faqs.append(new_faq)
    save_json(FAQ_FILE, faqs)
    return {"success": True, "faq": new_faq}

@app.put("/update-faq")
def update_faq(request: FAQUpdate):
    faqs = load_json(FAQ_FILE)
    for i, faq in enumerate(faqs):
        if faq["id"] == request.id:
            faqs[i] = {"id": request.id, "question": request.question, "answer": request.answer}
            save_json(FAQ_FILE, faqs)
            return {"success": True, "faq": faqs[i]}
    raise HTTPException(status_code=404, detail="FAQ not found")

@app.delete("/delete-faq/{faq_id}")
def delete_faq(faq_id: int):
    faqs = load_json(FAQ_FILE)
    faqs = [faq for faq in faqs if faq["id"] != faq_id]
    save_json(FAQ_FILE, faqs)
    return {"success": True}

@app.get("/unanswered")
def get_unanswered():
    return load_json(QUERIES_FILE)

@app.delete("/clear-unanswered/{query_id}")
def clear_unanswered(query_id: int):
    queries = load_json(QUERIES_FILE)
    queries = [q for q in queries if q["id"] != query_id]
    save_json(QUERIES_FILE, queries)
    return {"success": True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)