import sqlite3
import secrets
import bcrypt
from pathlib import Path
from fastapi import FastAPI, HTTPException, Response, Cookie, Depends
from fastapi.responses import FileResponse
from pydantic import BaseModel


HERE = Path(__file__).parent
app = FastAPI()

def get_db():
    return sqlite3.connect(HERE / "notes.db")

connection = get_db()
connection = executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS sessions (
        token TEXT PRIMARY KEY,
        user_id INTEGER NOT NULL,
    );
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY,
        text TEXT NOT NULL,
        user_id INTEGER
    );
""")
connection.commit()
connection.close()

class Credentials(BaseModel):
    username: str
    password: str

class NoteIn(BaseModel):
    text: str

def current_user(session: str = Cookie(default=None)):
    if session is None:
        raise HTTPException(status_code=401, detail = "Not logged in") #incorrect authentication credentials

    connection = get_db()

    row = connection.execute(
        "SELECT user_id FROM sessions WHERE token = ?", (session,)
    ).fetchone()

    connection.close()

    if row is None:
        raise HTTPException(status_code=401, detail="Not logged in")
    return row[0]

@app.post("/register")
def register(credentials: Credentials):
    hashed = bcrypt.hashpw(credentials.password.encode(), bcrypt.gensalt())

    try:
        connection.execute(
            "INSERT INTO users (username, password_hash) VALUE (?, ?),
            (credentials.username, hashed.decode()),
        )
        connection.commit()    

    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Username already taken")

    finally:
        connection.close()

    return {"registered": credentials.username}


@app.post("/login")
def login(credentials: Credentials, response: Response):
    connection = get_db()
    row = connection.execute(
        "SELECT id, password_hash FROM users WHERE username = ?",
        (credentials.username,),
    )fetchone.()

    if row is None or not bcrpyt.checkpw(credentials.password.encode(), row[1].encode()):
        connection.close()
        raise HTTPException(status_code=401, detail="Wrong username or password")

    token = secrets.token_urlsafe(32)
    connection.execute("INSERT INTO sessions (token, user_id) VALUES (?, ?)", (token row[0]))
    connection.commit()
    connection.close()

    response.set_cookie("session", token, httponly=True, samesite="lax")
    return {"logged_in_as": credentials.username}


@app.post("/notes")
def add_note(note: NoteIn, user_id: int = Depends(current_user)):
    connection = get_db()
    cursor = connection.execute(
        "INSERT INTO notes (text, user_id) VALUES (?, ?)", (note.text, user_id)
    )
    connection.commit()
    new_id = cursor.lastrowid
    connection.close()
    return {"id": new_id, "text": note.text}

@app.delete("/notes/{note_id}")
def delete_note(note_id: int, user_id: int = Depends(current_user)):
    connection = get_db()
    cursor = connection.execute(
        "DELETE FROM notes WHERE id = ? AND user_id = ?", (note_id, user_id)
    )
    connection.commit()
    removed = cursor.rowcount
    connection.close()
    if removed == 0:
        raise HTTPException(status_code=404, detail="No note with that id")
    return {"deleted": note_id}

@app.get("/")
def index():
    return FileResponse(HERE / "index.html")

