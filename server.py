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
        "SELECT id, password_hash"
    )
                                                                              