const input = document.getElementById("todoInput");
const button = document.getElementById("addButton");
const todoList = document.getElementById("todoList");

async function loadTodos() {
    const response = await fetch("/api/todos");
    const todos = await response.json();

    todoList.innerHTML = "";

    todos.forEach(todo => {
        addTodoToPage(todo);
    });
}

function addTodoToPage(todo) {
    const li = document.createElement("li");

    li.textContent = todo.text;

    const deleteButton = document.createElement("button");
    deleteButton.textContent = "Sil";

    deleteButton.addEventListener("click", async function () {
        await fetch(`/api/todos/${todo.id}`, {
            method: "DELETE"
        });

        loadTodos();
    });

    li.appendChild(deleteButton);
    todoList.appendChild(li);
}

button.addEventListener("click", async function () {
    const text = input.value.trim();

    if (text === "") {
        return;
    }

    await fetch("/api/todos", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            text: text
        })
    });

    input.value = "";

    loadTodos();
});

loadTodos();