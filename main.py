from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from rag import generate_answer, insert_resume

app = FastAPI()

class ResumeContent(BaseModel):
    section: str
    subsection: Optional[str] = None
    content: str

@app.get("/")
def home():
    return {"message": "RAG chatbot running"}


@app.post("/add-note")
def add_note(note: ResumeContent):
    insert_resume(note)
    return {"message": "Note added successfully"}

@app.get("/chat")
def chat(query: str):
    answer = generate_answer(query)
    return {"response": answer}