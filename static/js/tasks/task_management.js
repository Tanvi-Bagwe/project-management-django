/**
 * TASK CREATION HANDLER
 * Purpose: Handles the asynchronous submission of the task form using Fetch API.
 * This script manages validation, server communication, and UI feedback.
 */

function createTask() {
    const alertBox = document.getElementById("alertBox");
    const taskModal = document.getElementById("taskModal");

    // Clear previous alerts before starting a new request
    alertBox.innerHTML = "";

    const form = document.getElementById("taskForm");
    const formData = new FormData(form);

    // 1. CLIENT-SIDE VALIDATION
    // Ensure essential fields are not empty before hitting the server
    const title = formData.get("title").trim();
    const description = formData.get("description").trim();
    const project = formData.get("project_id");

    if (!title || !description || !project) {
        showAlert("warning", "Missing Information: Please ensure title and project are provided.");
        return;
    }

    // 2. FETCH CONFIGURATION
    // We retrieve the URL and Token directly from the form/DOM to keep this file generic
    const targetUrl = form.getAttribute("data-url");
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(targetUrl, {
        method: "POST",
        headers: {
            "X-CSRFToken": csrfToken,
            "X-Requested-With": "XMLHttpRequest" // Helps Django identify it as an AJAX request
        },
        body: formData
    })
        .then(response => {
            // 3. HTTP STATUS CHECKING
            // fetch() doesn't throw errors for 400/500 status codes. We must check manually.
            if (!response.ok) {
                return response.json().then(data => {
                    // If the server provided a specific error message, use it
                    throw new Error(data.message || `Server Error: ${response.status}`);
                }).catch(() => {
                    // Fallback if the server didn't return valid JSON (e.g., a 500 crash)
                    throw new Error("Critical Server Error. Please try again later.");
                });
            }
            return response.json();
        })
        .then(data => {
            // 4. SUCCESS HANDLING
            // Show the Bootstrap modal and reset the form for the next task
            const modalInstance = new bootstrap.Modal(taskModal);
            modalInstance.show();
            form.reset();
        })
        .catch(error => {
            // 5. GLOBAL ERROR CATCHING
            // Catches network failures, JSON parsing errors, and thrown errors from above
            console.error("Task Creation Failed:", error);
            showAlert("danger", `Failed to create task: ${error.message}`);
        });
}

/**
 * UI HELPER: Display Bootstrap Alerts
 * @param {string} type - 'success', 'warning', or 'danger'
 * @param {string} message - The text to display
 */
function showAlert(type, message) {
    const icon = type === 'danger' ? 'bi-exclamation-octagon' : 'bi-info-circle';
    document.getElementById("alertBox").innerHTML = `
        <div class="alert alert-${type} alert-dismissible fade show d-flex align-items-center" role="alert">
            <i class="bi ${icon} me-2"></i>
            <div>${message}</div>
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
}