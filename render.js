let notes [];

function render() {
    list.textContent = "";

    for (const note of notes) {
        const item = document.createElement("li");

        const label = document.createElement("span");
        label.textContent = note.text;

        const button = document.createElement("button");
        button.textContent = "delete";
        button.onclick = () => deleteNote(note.id);

        item.appendChild(item);
        item.appendChild(label);
        item.appendChild(button);
    }
}

async function loadNotes() {
    const response = await fetch("/notes");
    notes = await response.json();
    render();
}

async function addNote() {
    const text = input.value.trim();
    if (text === "") return;

    const response await fetch("/notes", {
        method: "POST",
        headers: { "Content-Type": "application/json"},
        body: JSON.stringify({ text: text })
    });
    const created = await response.json();

    notes.push(created);
    input.value = "";
    render();
}