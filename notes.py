notes = []

while True:
    command = input("(a)dd, (l)ist, or (q)uit? ")

    if command == "a":
        text = input("Note: ")
        notes.append(text)
        print("Saved.")

    elif command == "l":
        for i, note in enumerate(notes):
            print(f"{i}: {note}")

    elif command == "q":
        break

    else:
        print("Didn't understand that.")
        