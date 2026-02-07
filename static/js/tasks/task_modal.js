/**
 * ASYNCHRONOUS TASK CREATION (MODAL VERSION)
 * Purpose: Captures modal form data, validates it, and sends it to Django
 * without a full page refresh until the data is successfully saved.
 */

function createTask() {
    const alertBox = document.getElementById("alertBox");
    const form = document.getElementById("taskForm");
    const modalElement = document.getElementById("taskModal");

    // 1. UI STATE PREPARATION
    // Clear old errors and get the Bootstrap Modal instance
    alertBox.innerHTML = "";
    const modalInstance = bootstrap.Modal.getOrCreateInstance(modalElement);

    // 2. DATA EXTRACTION
    // FormData automatically collects all named inputs (title, project_id, etc.)
    const formData = new FormData(form);
    const title = formData.get("title").trim();
    const description = formData.get("description").trim();

    // 3. FRONT-END VALIDATION
    // Stops the request early if required fields are blank to save server bandwidth
    if (!title || !description) {
        showAlert("warning", "Input Required: Please fill in both the task title and description.");
        return;
    }

    // 4. SERVER COMMUNICATION (FETCH API)
    // We grab the URL from the form's data attribute to avoid hardcoding paths
    const postUrl = form.getAttribute("data-url");
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(postUrl, {
        method: "POST",
        headers: {
            "X-CSRFToken": csrfToken,
            "X-Requested-With": "XMLHttpRequest"
        },
        body: formData // Sends the form data as a multipart/form-data object
    })
        .then(response => {
            // 5. SERVER RESPONSE VALIDATION
            if (response.ok) {
                return response.json();
            } else {
                // If server returns an error (like 400 Bad Request), parse the error message
                return response.json().then(errData => {
                    throw new Error(errData.message || "Something went wrong on the server.");
                });
            }
        })
        .then(data => {
            // 6. SUCCESS FLOW
            // Hide modal, clear the form, and reload the page to show the new task
            modalInstance.hide();
            form.reset();
            window.location.reload();
        })
        .catch(error => {
            // 7. EXCEPTION HANDLING
            // Shows a danger alert if the network fails or server crashes
            console.error('Task Creation Error:', error);
            showAlert("danger", "Process Failed: " + error.message);
        });
}

/**
 * UTILITY: Display Dynamic Alerts inside the Modal
 */
function showAlert(type, message) {
    const alertBox = document.getElementById("alertBox");
    alertBox.innerHTML = `
        <div class="alert alert-${type} alert-dismissible fade show d-flex align-items-center" role="alert">
            <i class="bi bi-info-circle-fill me-2"></i>
            <div>${message}</div>
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
}