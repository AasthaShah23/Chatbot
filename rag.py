from embeddings import get_embedding
from google import genai
import os
from dotenv import load_dotenv
from db import engine
from sqlalchemy import text

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def search_similar(query):
    embedding = get_embedding(query)

    # convert list → string format for pgvector
    embedding_str = "[" + ",".join(map(str, embedding)) + "]"

    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT content
                FROM tech_notes
                ORDER BY embedding <-> CAST(:embedding AS vector)
                LIMIT 5
            """),
            {"embedding": embedding_str}
        )

        return [row[0] for row in result]

def generate_answer(query):
    docs = search_similar(query)

    context = "\n".join(docs)

    final_prompt = f"""
You are a helpful assistant.

Answer the question using ONLY the context below.

Give a clear and complete sentence.

Context:
{context}

Question: {query}
"""

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=final_prompt
    )

    return response.text

def insert_note(content):
    embedding = get_embedding(content)

    with engine.connect() as conn:
        conn.execute(
            text("""
                INSERT INTO tech_notes (content, embedding)
                VALUES (:content, :embedding)
            """),
            {"content": content, "embedding": embedding}
        )
        conn.commit()