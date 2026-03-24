# 🚀 AskBot – AI Chatbot Application

AskBot is a full-stack AI chatbot application with a **FastAPI backend** and a **React frontend**. It allows users to interact with an intelligent chatbot interface.

---

## 📁 Project Structure

```
Askbot-main/
│
├── backend/        # FastAPI backend
├── frontend/       # React frontend
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ Prerequisites

Make sure you have installed:

* Python 3.10+
* Node.js & npm
* Git

---

## 🚀 Backend Setup (FastAPI)

### 1️⃣ Navigate to backend folder

```bash
cd backend
```

### 2️⃣ Create virtual environment

```bash
python -m venv venv
```

### 3️⃣ Activate virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

**Mac/Linux:**

```bash
source venv/bin/activate
```

---

### 4️⃣ Install dependencies

```bash
pip install -r ../requirements.txt
```

---

### 5️⃣ Run backend server

```bash
uvicorn main:app --reload
```

👉 Backend will run at:

```
http://127.0.0.1:8000
```

---

## 🌐 Frontend Setup (React)

### 1️⃣ Open new terminal and navigate

```bash
cd frontend
```

### 2️⃣ Install dependencies

```bash
npm install
```

### 3️⃣ Run frontend

```bash
npm start
```

👉 Frontend will run at:

```
http://localhost:3000
```

---

## 🔗 API Documentation

Once backend is running:

* Swagger UI: http://127.0.0.1:8000/docs
* ReDoc: http://127.0.0.1:8000/redoc

---

## 🧠 Features

* AI chatbot interaction
* FastAPI backend APIs
* React-based UI
* Real-time responses
* Modular architecture

---

## ⚠️ Important Notes

* Do NOT upload `venv/` folder to GitHub
* Always use `.gitignore`
* Install dependencies using `requirements.txt`

---

## 📌 How to Run (Quick Summary)

```bash
# Backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r ../requirements.txt
uvicorn main:app --reload

# Frontend
cd frontend
npm install
npm start
```

---

## 👨‍💻 Author

Developed by **My Team**

---
