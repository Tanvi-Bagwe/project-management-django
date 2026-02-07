/**
 * PASSWORD RESET REQUEST HANDLER
 * Purpose: Validates the user's email format on the client side before
 * hitting the server. This prevents unnecessary database lookups for
 * incorrectly formatted email addresses.
 */

document.addEventListener('DOMContentLoaded', function () {
    const resetForm = document.getElementById("resetForm");

    if (resetForm) {
        resetForm.onsubmit = function (e) {
            // 1. Reset the UI
            const alertBox = document.getElementById("alertBox");
            alertBox.innerHTML = "";

            const email = this.email.value.trim();

            // 2. RUN VALIDATION
            // If the email is empty or fails the Regex test, we stop the submit event
            if (!email || !validateEmail(email)) {
                e.preventDefault(); // This stops the form from reloading the page
                showAlert("danger", "Invalid Input: Please provide a properly formatted email address.");
            }

            // If valid, the browser continues with the standard POST request to Django
        };
    }
});

/**
 * UI HELPER: Creates a Bootstrap alert dynamically
 */
function showAlert(type, message) {
    const alertBox = document.getElementById("alertBox");
    alertBox.innerHTML = `
        <div class="alert alert-${type} alert-dismissible fade show d-flex align-items-center" role="alert">
            <i class="bi bi-exclamation-circle-fill me-2"></i>
            <div>${message}</div>
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
}

/**
 * EMAIL REGEX UTILITY
 * Logic: Checks for [characters] + @ + [characters] + . + [characters]
 */
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}