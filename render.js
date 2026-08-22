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

