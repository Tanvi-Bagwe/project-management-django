/**
 * TASK ACTIONS HANDLER
 * Purpose: Manages destructive actions for tasks, such as deletion.
 * It uses a global variable to track the task selected for deletion via
 * a confirmation modal, ensuring the user doesn't delete by mistake.
 */

// Global variable to keep track of which task the user clicked
let deleteTaskId = null;

/**
 * TRIGGER: Called when the trash icon is clicked in the task table.
 */
function confirmDelete(id) {
    deleteTaskId = id;

    // Select the modal element and show it using the Bootstrap API
    const modalElement = document.getElementById("deleteTaskModal");
    const modalInstance = bootstrap.Modal.getOrCreateInstance(modalElement);
    modalInstance.show();
}

/**
 * EXECUTION: Sends the DELETE request to the Django server.
 */
function deleteTask() {
    // 1. UI FEEDBACK
    // Disable the delete button so the user can't click it twice
    const deleteBtn = document.querySelector("#deleteTaskModal .btn-danger");
    deleteBtn.disabled = true;
    deleteBtn.innerText = "Deleting...";

    // 2. RETRIEVE DATA
    // We get the CSRF token from the hidden input field Django provides
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // 3. API CALL
    // We use the 'DELETE' method which is the standard for removing resources
    fetch(`/tasks/delete/${deleteTaskId}/`, {
        method: "DELETE",
        headers: {
            "X-CSRFToken": csrfToken,
            "Accept": "application/json",
            "X-Requested-With": "XMLHttpRequest"
        }
    })
        .then(res => {
            // 4. SERVER RESPONSE VALIDATION
            if (!res.ok) {
                return res.json().then(data => {
                    throw new Error(data.message || "Deletion failed on server.");
                });
            }
            return res.json();
        })
        .then(data => {
            // 5. SUCCESS FLOW
            // Reload the page to show the updated task list
            location.reload();
        })
        .catch(error => {
            // 6. ERROR LOGGING
            console.error("Task Deletion Error:", error);
            alert("Action Failed: " + error.message);

            // Reset the button if it fails
            deleteBtn.disabled = false;
            deleteBtn.innerText = "Delete";
        });
}