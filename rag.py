from embeddings import get_embedding
from google import genai
import os
from dotenv import load_dotenv
from db import engine
from sqlalchemy import text

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

from sqlalchemy import text

def search_similar(query):
    embedding = get_embedding(query)

    # convert list → pgvector string
    embedding_str = "[" + ",".join(map(str, embedding)) + "]"

    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT section, subsection, content
                FROM resume_embeddings
                ORDER BY embedding <-> CAST(:embedding AS vector)
                LIMIT 5
            """),
            {"embedding": embedding_str}
        )

        rows = result.fetchall()

    # ✅ format context nicely
    formatted_docs = []
    for row in rows:
        section, subsection, content = row

        formatted = f"""
Section: {section}
Subsection: {subsection or "N/A"}
Content: {content}
"""
        formatted_docs.append(formatted.strip())

    return formatted_docs

def generate_answer(query):
    docs = search_similar(query)

    context = "\n\n---\n\n".join(docs)

    final_prompt = f"""
You are an AI assistant answering questions about a candidate's professional background.

STRICT RULES:
- Answer ONLY from the provided context
- Be specific and professional
- Do NOT say "I don't know" if answer exists in context
- Do NOT give generic AI answers
- Keep answer concise but complete

Context:
{context}

Question: {query}

Answer:
"""

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=final_prompt
    )

    return response.text


def insert_resume(entry):
    embedding = get_embedding(entry.content)

    with engine.connect() as conn:
        conn.execute(
            text("""
                INSERT INTO resume_embeddings (section, subsection, content, embedding)
                VALUES (:section, :subsection, :content, :embedding)
            """),
            {
                "section": entry.section,
                "subsection": entry.subsection,
                "content": entry.content,
                "embedding": embedding
            }
        )
        conn.commit()