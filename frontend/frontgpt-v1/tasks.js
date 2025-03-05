const API_URL = "http://localhost:8765/v1/api";

async function fetchTasks() {
    const res = await fetch(`${API_URL}/tasks/list`, {
        method: "GET",
        credentials: "include"
    });

    if (res.ok) {
        const data = await res.json();
        const taskList = document.getElementById("taskList");
        taskList.innerHTML = "";

        data.tasks.forEach(task => {
            if (task.mode !== "deleted") {
                const li = document.createElement("li");
                li.innerHTML = `${task.name} (${task.mode})
                    <button onclick="changeTaskMode(${task.id}, 'completed')">Завершить</button>
                    <button onclick="deleteTask(${task.id})">Удалить</button>`;
                taskList.appendChild(li);
            }
        });
    }
}

async function createTask() {
    const taskName = document.getElementById("newTask").value;

    await fetch(`${API_URL}/tasks/create`, {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: taskName })
    });

    fetchTasks();
}

async function changeTaskMode(taskId, mode) {
    await fetch(`${API_URL}/tasks/change-mode`, {
        method: "PATCH",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ taskid: taskId, mode })
    });

    fetchTasks();
}

async function deleteTask(taskId) {
    await changeTaskMode(taskId, "deleted");
}

async function pingServer() {
    const res = await fetch(`${API_URL}/ping`);
    if (res.ok) {
        const data = await res.json();
        document.getElementById("serverStatus").innerText = `Сервер работает: ${data.uptime} секунд`;
    } else {
        document.getElementById("serverStatus").innerText = "Ошибка соединения с сервером";
    }
}

// Загружаем задачи при открытии страницы
fetchTasks();
