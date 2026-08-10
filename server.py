import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

def get_db():
    return sqlite3.connect("notes.db")

connection = get_db()
connection.execute("""
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY,
        text TEXT NOT NULL
    )
""")
connection.commit()
connection.close()

class NoteIn(BaseModel):
    text: str

@app.get("/notes")
def list_notes():
    connection = get_db()
    rows = connection.execute("SELECT id, text FROM notes").fetchall()
    connection.close()
    return [{"id": row[0], "text": row[1]} for row in rows]

@app.post("/notes")
def add_note(note: NoteIn):
    connection = get_db()
    cursor = connection.execute("INSERT INTO notes (text) VALUES (?)", (note.text,))
    connection.commit()
    new_id = cursor.lastrowid
    connection.close()
    return {"id": new_id, "text": note.text}


@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    connection = get_db()
    cursor = connection.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    connection.commit()
    removed = cursor.rowcount
    connection.close()
    if removed == 0:
        raise HTTPException(status_code=404, detail="No note with that id")
    return {"deleted": note_id}
