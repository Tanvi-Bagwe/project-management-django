/**
 * USER MANAGEMENT SYSTEM
 * Purpose: This script handles administrative actions like enabling or
 * disabling user accounts asynchronously.
 * Note: We use a single shared modal for all user cards to keep the DOM clean.
 */

// We use this to track which user was clicked on for the modal's confirmation
let selectedUserId = null;

/**
 * INITIALIZATION: Set up the Bootstrap Modal instance once the page loads.
 */
document.addEventListener('DOMContentLoaded', function () {
    const modalElement = document.getElementById('confirmModal');
    // Store the modal in a way that we can access it from other functions
    window.userStatusModal = new bootstrap.Modal(modalElement);

    // Attach the click event to the confirm button inside the modal
    document.getElementById("confirmBtn").onclick = function () {
        if (selectedUserId) {
            toggleUser(selectedUserId);
        }
    };
});

/**
 * TRIGGER: Called when the 'Enable/Disable' button is clicked on a user card.
 * @param {number} id - The ID of the user to be modified.
 */
function showConfirmModal(id) {
    selectedUserId = id;
    if (window.userStatusModal) {
        window.userStatusModal.show();
    }
}

/**
 * EXECUTION: The actual API call to the Django backend.
 * Logic: Sends a POST request to the toggle endpoint and reloads the page on success.
 */
function toggleUser(id) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const confirmBtn = document.getElementById("confirmBtn");

    // Feedback: Disable button to prevent multiple clicks during processing
    confirmBtn.disabled = true;
    confirmBtn.innerText = "Processing...";

    fetch(`/users/${id}/toggle/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": csrfToken,
            "X-Requested-With": "XMLHttpRequest"
        }
    })
        .then(response => {
            if (response.ok) {
                // Success: Refresh the page to show the updated account status badges/buttons
                location.reload();
            } else {
                // Error Handling: Extract error message if provided by Django
                return response.json().then(data => {
                    throw new Error(data.message || "Unable to update user status.");
                });
            }
        })
        .catch(error => {
            console.error("Admin Action Failed:", error);
            alert("Action Failed: " + error.message);

            // Reset UI if it fails so the admin can try again
            confirmBtn.disabled = false;
            confirmBtn.innerText = "Confirm";
        });
}