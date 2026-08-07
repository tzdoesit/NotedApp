
import sqlite3

connection = sqlite3.connect("notes.db")
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY,
        text TEXT NOT NULL
    )
""")
connection.commit()


while True:
    command = input("(a)dd, (l)ist, or (q)uit? ")

    if command == "a":
        text = input("Note: ")
        cursor.execute("INSERT INTO notes (text) VALUES (?)", (text,))
        connection.commit()
        print("Saved.")

    elif command == "l":
        cursor.execute("SELECT id, text FROM notes")
        for row in cursor.fetchall():
            print(f"{row[0]}: {row[1]}")

    elif command == "q":
        break

    else:
        print("Didn't understand that.")


connection.close()