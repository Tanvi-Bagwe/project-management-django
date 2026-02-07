/**
 * PROJECT DELETION SYSTEM
 * Purpose: Handles the 'Dangerous' action of deleting a project via AJAX.
 * I used a global variable to track the ID because the modal is shared
 * across all project cards on the page.
 */

// Global variable to store the ID of the project we clicked on
let projectIdToDelete = null;

/**
 * Function: openDeleteModal
 * Triggered by the trash icon on the UI.
 * It "remembers" the project ID and pops up the warning modal.
 */
function openDeleteModal(id) {
    projectIdToDelete = id;

    // Check if Bootstrap is loaded to avoid console crashes
    if (typeof bootstrap !== 'undefined') {
        const modalElement = document.getElementById('deleteModal');
        const modalInstance = bootstrap.Modal.getOrCreateInstance(modalElement);
        modalInstance.show();
    } else {
        console.error("Bootstrap JS not found. Cannot show modal.");
    }
}

/**
 * Event Listener for the Confirmation Button
 * This runs once the DOM is ready to attach the click event to the 'Delete Permanently' button.
 */
document.addEventListener('DOMContentLoaded', function () {
    const confirmBtn = document.getElementById("confirmDeleteBtn");

    if (confirmBtn) {
        confirmBtn.onclick = function () {
            if (projectIdToDelete) {
                executeDelete(projectIdToDelete);
            }
        };
    }
});

/**
 * Function: executeDelete
 * The actual API call. Uses the DELETE method which is more RESTful.
 */
function executeDelete(id) {
    // Get the CSRF token from the hidden input Django provides in the template
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const deleteBtn = document.getElementById("confirmDeleteBtn");

    // Disable button and change text to show "Processing..."
    deleteBtn.disabled = true;
    deleteBtn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Deleting...';

    // Constructing the URL dynamically using backticks
    fetch(`/projects/${id}/delete/`, {
        method: "DELETE",
        headers: {
            "X-CSRFToken": csrfToken,
            "Content-Type": "application/json",
            "X-Requested-With": "XMLHttpRequest"
        }
    })
        .then(response => {
            // Checking if the server actually deleted the record (Status 200-299)
            if (response.ok) {
                // Refresh the page to show the project is gone
                location.reload();
            } else {
                // Error handling if the user doesn't have permission or DB fails
                return response.json().then(data => {
                    throw new Error(data.message || "Delete failed due to server error.");
                });
            }
        })
        .catch(error => {
            console.error("Critical Error during deletion:", error);
            alert("System Error: " + error.message);

            // Reset the button if it fails so the user can try again
            deleteBtn.disabled = false;
            deleteBtn.innerHTML = "Delete Permanently";
        });
}