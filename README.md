# 🤖 AI-Powered Personal Chatbot (RAG + pgvector + FastAPI)

An AI chatbot that answers recruiter questions about your professional background using **Retrieval-Augmented Generation (RAG)** with **PostgreSQL + pgvector**.

Instead of hardcoded responses, this chatbot retrieves relevant information from your stored experience and generates **context-aware, first-person answers**.

---

## 🚀 Features

* 🧠 Context-aware responses using RAG
* 🔍 Semantic search with pgvector
* ⚡ FastAPI backend
* 📡 Add data dynamically via API
* 🎯 Interview-style responses (first-person answers)

---

## 🏗️ Tech Stack

* Python (FastAPI)
* PostgreSQL + pgvector
* OpenAI API (embeddings + responses)
* psycopg2

---

## 📁 Project Structure

```bash
.
├── db.py                # Database connection
├── embeddings.py        # Embedding generation logic
├── rag.py               # Retrieval logic (similarity search)
├── main.py              # FastAPI app     
├── .env.example         # Environment variables
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

---

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/AasthaShah23/Chatbot.git
cd Chatbot
```

---

### 2️⃣ Create Virtual Environment

#### 🟢 Mac / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

#### 🪟 Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🗄️ Setup PostgreSQL + pgvector

---

### 🔹 Install PostgreSQL

#### 🟢 Mac (Homebrew)

```bash
brew install postgresql@16
brew services start postgresql@16
```

#### 🪟 Windows

* Download from: https://www.postgresql.org/download/windows/
* Install via GUI

#### 🐧 Linux (Ubuntu)

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

---

### 🔹 Install pgvector

#### 🟢 Mac

```bash
brew install pgvector
```

#### 🐧 Linux

```bash
git clone https://github.com/pgvector/pgvector.git
cd pgvector
make
sudo make install
```

#### 🪟 Windows

👉 Recommended: Use Docker

```bash
docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=postgres ankane/pgvector
```

---

### 🔹 Restart PostgreSQL

```bash
brew services restart postgresql@16   # Mac
sudo systemctl restart postgresql     # Linux
```

---

## 🧠 Database Setup

Open PostgreSQL (psql / Postico / pgAdmin)

```sql
CREATE DATABASE chatbot;

CREATE EXTENSION vector;
```

---

## 📦 Create Table

```sql
CREATE TABLE resume_embeddings (
    id SERIAL PRIMARY KEY,
    section TEXT NOT NULL,
    subsection TEXT NULL,
    content TEXT NOT NULL,
    embedding VECTOR(3072)
);
```

---

## 🔐 Environment Variables

Create `.env`:

```env
OPENAI_API_KEY=
DATABASE_URL=
```

---

## ▶️ Run the Server

```bash
uvicorn main:app --reload
```

👉 Server:

```
http://127.0.0.1:8000
```

---

## 📡 Add Data (NEW FLOW)

You are now adding data via API.

### Endpoint:

```
POST /add-note
```

### Request Body:

```json
{
  "section": "experience",
  "subsection": "backend",
  "content": "Add context according to your data"
}
```

👉 This will:

* Generate embedding
* Store data in PostgreSQL

---

## 💬 Ask Questions

### Endpoint:

```
POST /chat
```

### Request Body:

```json
{
  "question": "Tell me about your backend experience"
}
```

---

## 🧠 How It Works

1. Your data → converted into embeddings 
2. Stored in pgvector 
3. User question → converted into embedding 
4. Similar data retrieved using vector search 
5. Context + question → sent to LLM 
6. AI generates answer

---

## 🎯 Example Response

```
"I have experience in backend development where I built secure certificate exchange APIs using Catena-X and worked on scalable system design."
```

---

## ⚠️ Common Issues

### ❌ `vector extension not available`

→ pgvector not installed properly OR version mismatch

### ❌ `type vector does not exist`

→ Run: `CREATE EXTENSION vector;`

### ❌ No results in chat

→ Ensure data is inserted via `/add-note`

---

## 💡 Pro Tips

* Keep content meaningful (2–4 sentences per entry)
* Avoid very small or very large chunks
* Use clear, descriptive language

---
