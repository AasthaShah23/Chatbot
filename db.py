from sqlalchemy import create_engine

DATABASE_URL = "postgresql://aasthashah:hello@localhost:5432/Chatbot_RAG"

engine = create_engine(DATABASE_URL)

