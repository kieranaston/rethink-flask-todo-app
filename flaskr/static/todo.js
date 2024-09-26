/* Changes the default form submission behaviour to instead call the addTodo() function,
which in turn sends a POST request with the contents to the backend. */
document.getElementById('todo-form').addEventListener('submit', function(event) {
    event.preventDefault();
    addTodo()
})

/* Dynamically sorts todos in-place on the page.
This is called whenever a todo is toggled so that
there is no need to get all the todo items from the database
again when a single item changes. Uses the same sorting logic as the
backed so that even when the page is refreshed the ordering is consistent. */
function sortTodos() {
    const todoList = document.getElementById('todo-list');
    const todoItems = Array.from(todoList.children);
    todoItems.sort((a, b) => {
        const aCompleted = a.querySelector('input[type="checkbox"]').checked;
        const bCompleted = b.querySelector('input[type="checkbox"]').checked;
        if (aCompleted !== bCompleted) {
            return aCompleted - bCompleted;
        }
        const aDate = new Date(a.getAttribute('creation-date'));
        const bDate = new Date(b.getAttribute('creation-date'));
        return bDate - aDate;
    });
    todoItems.forEach(item => todoList.appendChild(item));
}

/* Gets the data from the submitted form as a FormData object and
sends it to the backend along with a "created at" attribute for
sorting purposes. */
function addTodo() {
    const form = new FormData(document.getElementById("todo-form"));
    const title = form.get("title");
    const createdAt = new Date().toISOString();
    const todo = {"title": title, "completed": false, "created_at": createdAt};
    fetch(newTodoUrl, {
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "body": JSON.stringify(todo),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Failed to add todo. Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log("Todo added successfully:", data);
        const todoList = document.getElementById("todo-list");
        const div = document.createElement('div');
        div.id = `todo-item-${data.id}`;
        div.setAttribute('creation-date', createdAt);
        div.innerHTML = `
            <input type="checkbox" id="${data.id}" ${todo.completed ? 'checked' : ''} onchange="toggleTodo('${data.id}')">
            <label for="${data.id}">${todo.title}</label>
            <button onclick="deleteTodo('${data.id}')">Delete</button>
        `;
        todoList.insertBefore(div, todoList.firstChild);
        document.getElementById("todo-form").reset();
    })
    .catch(error => {
        console.error("Error adding todo:", error.message);
        alert(`There was a problem adding the todo: ${error.message}`);
    });
}

/* Gets todos from the database.
The fetched todos are all contained within a div object,
and each one gets its own div object with id and timestamp
attributes to support the client-side sorting. */
function getTodos() {
    const todoList = document.getElementById("todo-list");
    fetch(getTodosUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Failed to fetch todos. Status: ${response.status}`);
            }
            return response.json();
        })
        .then(todos => {
            console.log("Fetched todos:", todos);
            if (!Array.isArray(todos)) {
                throw new Error("Unexpected response format: todos should be an array.");
            }
            todoList.innerHTML = '';
            todos.forEach(todo => {
                const div = document.createElement('div');
                div.id = `todo-item-${todo.id}`;
                div.setAttribute('creation-date', todo.created_at);
                div.innerHTML = `
                    <input type="checkbox" id="${todo.id}" ${todo.completed ? 'checked' : ''} onchange="toggleTodo('${todo.id}')">
                    <label for="${todo.id}">${todo.title}</label>
                    <button onclick="deleteTodo('${todo.id}')">Delete</button>
                `;
                todoList.appendChild(div);
            });
        })
        .catch(error => {
            console.error("Error fetching todos:", error.message);
            alert(`There was a problem fetching the todo list: ${error.message}`);
        });
}

/* Todos can be toggled to indicate complete/not complete. */
function toggleTodo(id) {
    const todoElement = document.getElementById(id);
    if (!todoElement) {
        console.error(`Todo element with id ${id} not found`);
        return;
    }
    const completed = todoElement.checked;
    fetch(`/todos/${id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ completed }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Errpr(`Failed to update todo. Status: ${response.status}`);
        }
        todoElement.setAttribute('completed', completed);
        sortTodos();
    })
    .catch(error => {
        console.error("Error updating todo:", error.message);
        alert(`THere was a problem updating the todo: ${error.message}`);
    });
}

/* Delete a todo. */
function deleteTodo(id) {
    fetch(`/todos/${id}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to delete the todo');
        }
        const todoItem = document.getElementById(`todo-item-${id}`);
        if (todoItem) {
            todoItem.remove();
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

/* Calls the getTodos() function on page load. */
window.onload = function() {
    getTodos();
}
