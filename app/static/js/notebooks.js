let draggedItem = null;
let placeholder = null;

function editing_mode() {
    const container = document.getElementById("notebooks-container");

    container.classList.toggle("not-editing");
    container.classList.toggle("editing");

    updateDraggableStatus();

    const links = document.querySelectorAll(".notebook a");

    links.forEach(link => {
        link.style.pointerEvents = container.classList.contains("editing") ? "none" : "auto";
    });
}

function updateDraggableStatus() {
    const container = document.getElementById("notebooks-container");
    if (!container) return;
    const isEditing = container.classList.contains("editing");
    document.querySelectorAll(".task").forEach(item => item.draggable = isEditing);
    document.querySelectorAll(".task-status-checkbox").forEach(input => input.disabled = isEditing);
}

function updateTaskNumbers() {
    const tasks = document.querySelectorAll("#task-list .task");
    tasks.forEach((task, index) => {
        const number = task.querySelector(".list-number");
        if (number) number.textContent = String(index + 1).padStart(3, "0");
    });
}

function updateNotebookNumbers() {
    const notebooks = document.querySelectorAll("#notebooks-list .notebook");
    notebooks.forEach((notebook, index) => {
        const number = notebook.querySelector(".list-number");
        if (number) number.textContent = String(index + 1).padStart(3, "0");
    });
}

function updateTaskOrderInputs() {
    const tasks = document.querySelectorAll("#task-list .task");
    tasks.forEach(task => {
        const existingInput = task.querySelector("input[name='existing_tasks']");
        const orderInput = task.querySelector("input[name='task_order']");
        if (existingInput && orderInput) orderInput.value = existingInput.value;
    });
}

function updateTaskStatusInputs() {
    const tasks = document.querySelectorAll("#task-list .task");
    tasks.forEach(task => {
        const checkbox = task.querySelector(".task-status-checkbox");
        const statusInput = task.querySelector("input[name='task_status']");
        const existingInput = task.querySelector("input[name='existing_tasks']");
        if (checkbox && statusInput && existingInput) statusInput.value = `${existingInput.value}:${checkbox.checked ? 1 : 0}`;
    });
}

function updateTaskStatusOnDatabase(checkbox) {
    const taskId = checkbox.dataset.taskId;
    if (!taskId) return;
    const formData = new FormData();
    formData.append("status", checkbox.checked);
    fetch(`/task/${taskId}/status`, {
        method: "POST",
        body: formData
    });
}

function addItem() {
    const input = document.getElementById("new-task-input");
    const taskList = document.getElementById("task-list");
    if (!input || !taskList) return;
    const value = input.value.trim();
    if (!value) return;
    const li = document.createElement("li");
    li.classList.add("task");
    li.draggable = document.getElementById("notebooks-container").classList.contains("editing");
    li.innerHTML = `<label><input type="checkbox" class="task-status-checkbox" disabled><span class="list-number"></span> - <span class="list-name"></span></label><input type="hidden" name="new_tasks" value=""><div class="edit-options"><button type="button" class="material-symbols-outlined btn delete-btn" onclick="removeItem(this)">delete</button></div>`;
    li.querySelector(".list-name").textContent = value;
    li.querySelector("input[name='new_tasks']").value = value;
    taskList.prepend(li);
    input.value = "";
    updateTaskNumbers();
    updateTaskOrderInputs();
}

function removeItem(button) {
    const task = button.closest(".task");
    if (!task) return;
    const existingInput = task.querySelector("input[name='existing_tasks']");
    if (existingInput) {
        const form = task.closest("form");
        const deletedInput = document.createElement("input");
        deletedInput.type = "hidden";
        deletedInput.name = "deleted_tasks";
        deletedInput.value = existingInput.value;
        form.appendChild(deletedInput);
    }
    task.remove();
    updateTaskNumbers();
    updateTaskOrderInputs();
    updateTaskStatusInputs();
}

function addNotebook() {
    const input = document.getElementById("new-notebook-input");
    const notebookList = document.getElementById("notebooks-list");
    if (!input || !notebookList) return;
    const value = input.value.trim();
    if (!value) return;
    const li = document.createElement("li");
    li.classList.add("notebook");
    li.innerHTML = `<span class="list-number"></span> - <span class="list-name"></span> - <span class="progress">0%</span><input type="hidden" name="new_notebooks" value=""><div class="edit-options"><button type="button" class="material-symbols-outlined btn delete-btn" onclick="removeNotebook(this)">delete</button></div>`;
    li.querySelector(".list-name").textContent = value;
    li.querySelector("input[name='new_notebooks']").value = value;
    notebookList.prepend(li);
    input.value = "";
    updateNotebookNumbers();
}

function removeNotebook(button) {
    const notebook = button.closest(".notebook");
    if (!notebook) return;
    const existingInput = notebook.querySelector("input[name='existing_notebooks']");
    if (existingInput) {
        const form = notebook.closest("form");
        const deletedInput = document.createElement("input");
        deletedInput.type = "hidden";
        deletedInput.name = "deleted_notebooks";
        deletedInput.value = existingInput.value;
        form.appendChild(deletedInput);
    }
    notebook.remove();
    updateNotebookNumbers();
}

function enableDragAndDrop(listSelector, itemSelector, updateNumbersFunction) {
    const list = document.querySelector(listSelector);
    if (!list) return;
    list.addEventListener("dragstart", event => {
        const item = event.target.closest(itemSelector);
        if (!item || !item.draggable) return;
        draggedItem = item;
        item.classList.add("dragging");
        placeholder = document.createElement("li");
        placeholder.classList.add("drag-placeholder");
        placeholder.style.height = `${item.offsetHeight}px`;
        const img = new Image();
        img.src = "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw==";
        event.dataTransfer.setDragImage(img, 0, 0);
        event.dataTransfer.effectAllowed = "move";
    });
    list.addEventListener("dragover", event => {
        event.preventDefault();
        if (!draggedItem || !placeholder) return;
        const afterElement = getDragAfterElement(list, event.clientY);
        if (afterElement == null) list.appendChild(placeholder);
        else list.insertBefore(placeholder, afterElement);
    });
    list.addEventListener("drop", event => {
        event.preventDefault();
        if (!draggedItem || !placeholder) return;
        placeholder.replaceWith(draggedItem);
        updateNumbersFunction();
        updateTaskOrderInputs();
    });
    list.addEventListener("dragend", () => {
        if (draggedItem) draggedItem.classList.remove("dragging");
        if (placeholder) placeholder.remove();
        draggedItem = null;
        placeholder = null;
        updateNumbersFunction();
        updateTaskOrderInputs();
    });
}

function getDragAfterElement(list, y) {
    const items = [...list.querySelectorAll("li:not(.dragging):not(.drag-placeholder)")];
    return items.reduce((closest, child) => {
        const box = child.getBoundingClientRect();
        const offset = y - box.top - box.height / 2;
        if (offset < 0 && offset > closest.offset) return { offset: offset, element: child };
        return closest;
    }, { offset: Number.NEGATIVE_INFINITY }).element;
}

document.addEventListener("DOMContentLoaded", () => {
    const taskInput = document.getElementById("new-task-input");
    if (taskInput) taskInput.addEventListener("keydown", event => {
        if (event.key === "Enter") {
            event.preventDefault();
            addItem();
        }
    });

    const notebookInput = document.getElementById("new-notebook-input");
    if (notebookInput) notebookInput.addEventListener("keydown", event => {
        if (event.key === "Enter") {
            event.preventDefault();
            addNotebook();
        }
    });

    document.querySelectorAll(".task-status-checkbox").forEach(input => input.addEventListener("change", () => {
        updateTaskStatusInputs();
        updateTaskStatusOnDatabase(input);
    }));

    enableDragAndDrop("#task-list", ".task", updateTaskNumbers);
    updateTaskNumbers();
    updateNotebookNumbers();
    updateDraggableStatus();
    updateTaskOrderInputs();
    updateTaskStatusInputs();
});