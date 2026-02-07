/**
 * PROJECT DASHBOARD ACTIONS
 * Purpose: Manages the creation of new projects via an asynchronous (AJAX)
 * request to ensure the user can create projects without full page reloads.
 */

/**
 * Function: createProject
 * Triggered by the 'Create' button inside the Project Modal.
 */
function createProject() {
    // 1. SELECT UI ELEMENTS
    const alertBox = document.getElementById("alertBox");
    const form = document.getElementById("projectForm");
    const createBtn = document.querySelector("#projectForm button");

    // Clear any previous alerts
    alertBox.innerHTML = "";

    // 2. DATA EXTRACTION
    // Use FormData to grab name and description from the form inputs
    const formData = new FormData(form);
    const name = formData.get("name").trim();
    const description = formData.get("description").trim();

    // 3. FRONT-END VALIDATION
    // Check if the fields are empty before sending to the server
    if (!name || !description) {
        showAlert("warning", "Required Fields: Please provide both a project name and a brief description.");
        return;
    }

    // 4. REQUEST EXECUTION
    // Grab the URL from the form's data attribute and the CSRF token from the DOM
    const postUrl = form.getAttribute("data-url");
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Show loading state
    createBtn.disabled = true;
    createBtn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Creating...';

    fetch(postUrl, {
        method: "POST",
        headers: {
            "X-CSRFToken": csrfToken,
            "X-Requested-With": "XMLHttpRequest"
        },
        body: formData
    })
        .then(res => {
            // 5. SERVER RESPONSE CHECK
            if (!res.ok) {
                return res.json().then(data => {
                    throw new Error(data.message || "Failed to create project.");
                });
            }
            return res.json();
        })
        .then(data => {
            // 6. SUCCESS HANDLING
            // Reload the dashboard to show the new project card
            window.location.reload();
        })
        .catch(err => {
            // 7. ERROR HANDLING
            console.error("Project Creation Error:", err);
            showAlert("danger", "System Error: " + err.message);

            // Reset button state on failure
            createBtn.disabled = false;
            createBtn.innerText = "Create";
        });
}

/**
 * UI HELPER: Display Bootstrap Alert
 */
function showAlert(type, message) {
    const alertBox = document.getElementById("alertBox");
    alertBox.innerHTML = `
        <div class="alert alert-${type} alert-dismissible fade show d-flex align-items-center" role="alert">
            <i class="bi bi-exclamation-triangle-fill me-2"></i>
            <div>${message}</div>
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
}