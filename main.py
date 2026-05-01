from fastapi import FastAPI
from pydantic import BaseModel
from rag import generate_answer, insert_note

app = FastAPI()

class Note(BaseModel):
    content: str

@app.get("/")
def home():
    return {"message": "RAG chatbot running"}


@app.post("/add-note")
def add_note(note: Note):
    insert_note(note.content)
    return {"message": "Note added successfully"}

@app.get("/chat")
def chat(query: str):
    answer = generate_answer(query)
    return {"response": answer}