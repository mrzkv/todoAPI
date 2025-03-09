const API_URL = "http://localhost:8765/v1/api/tasks";
document.addEventListener("DOMContentLoaded", loadTasks);

document.getElementById("addTaskBtn").addEventListener("click", createTask);
document.getElementById("logoutBtn").addEventListener("click", () => {
    document.cookie = "access_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    window.location.href = "auth.html";
});

document.getElementById("newTaskName").addEventListener("keypress", (event) => {
    if (event.key === "Enter") createTask();
});

async function loadTasks() {
    try {
        const response = await fetch(`${API_URL}/list`, {
            credentials: "include"
        });
        const data = await response.json();

        if (response.status >= 400) {
            alert(data.detail || "Ошибка загрузки задач");
            return;
        }

        const taskList = document.getElementById("taskList");
        taskList.innerHTML = "";

        data.tasks.forEach(task => {
            if (task.mode !== "deleted") {
                const li = document.createElement("li");
                li.innerHTML = `
                    <span>${task.name} (${task.mode})</span>
                    <button onclick="changeTaskMode(${task.id}, 'completed')">Завершить</button>
                    <button onclick="changeTaskMode(${task.id}, 'deleted')">Удалить</button>
                `;
                taskList.appendChild(li);
            }
        });

    } catch (error) {
        console.error("Ошибка загрузки задач:", error);
    }
}

async function createTask() {
    const taskName = document.getElementById("newTaskName").value.trim();
    if (!taskName) return;

    try {
        const response = await fetch(`${API_URL}/create`, {
            method: "POST",
            credentials: "include",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ name: taskName })
        });

        const data = await response.json();
        if (response.status >= 400) {
            alert(data.detail || "Ошибка создания задачи");
            return;
        }

        document.getElementById("newTaskName").value = "";
        loadTasks();
    } catch (error) {
        console.error("Ошибка создания задачи:", error);
    }
}

async function changeTaskMode(taskId, mode) {
    try {
        const response = await fetch(`${API_URL}/change-mode`, {
            method: "PATCH",
            credentials: "include",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ taskid: taskId, mode: mode })
        });

        const data = await response.json();
        if (response.status >= 400) {
            alert(data.detail || "Ошибка изменения задачи");
            return;
        }

        loadTasks();
    } catch (error) {
        console.error("Ошибка изменения задачи:", error);
    }
}
