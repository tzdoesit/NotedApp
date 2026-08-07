
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
    command = input("(a)dd, (l)ist, (d)elete, or (q)uit? ")

    if command == "a":
        text = input("Note: ")
        cursor.execute("INSERT INTO notes (text) VALUES (?)", (text,))
        connection.commit()
        print("Saved.")

    elif command == "l":
        cursor.execute("SELECT id, text FROM notes")
        for row in cursor.fetchall():
            print(f"{row[0]}: {row[1]}")

    elif command == "d":
        try:
            delete_note = input("Which note would you like to delete? ")
            int_to_delete = int(delete_note)
        except ValueError:
            print("That's not a number.")

        cursor.execute("DELETE FROM notes WHERE id = (?)", (int_to_delete,))
        connection.commit()
        if cursor.rowcount == 1:
            print("Your note has been deleted.")
        elif cursor.rowcount == 0:
            print("There is no note to delete.")
        else:
            print("Hmm, something weird happened")

    elif command == "q":
        break

    else:
        print("Didn't understand that.")


connection.close()