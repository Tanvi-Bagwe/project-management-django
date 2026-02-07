/**
 * PASSWORD VALIDATION AND SUBMISSION
 * Purpose: Ensures the user meets security requirements before sending data to the server.
 * This saves server resources by catching simple errors (like non-matching passwords) early.
 */

document.addEventListener('DOMContentLoaded', function () {
    const pwdForm = document.getElementById("pwdForm");

    if (pwdForm) {
        pwdForm.onsubmit = function (e) {
            // 1. CLEAR PREVIOUS ALERTS
            const alertBox = document.getElementById("alertBox");
            alertBox.innerHTML = "";

            const pass1 = this.new_password1.value;
            const pass2 = this.new_password2.value;

            // 2. STRENGTH VALIDATION
            // Uses a Regular Expression to check for:
            // ^(?=.*[A-Za-z]) -> At least one letter
            // (?=.*\d)        -> At least one number
            // [A-Za-z\d]{8,}$ -> At least 8 characters long
            if (!validatePassword(pass1)) {
                e.preventDefault(); // Stop the form from submitting
                showAlert("warning", "Security Requirement: Password must be at least 8 characters and include both letters and numbers.");
                return;
            }

            // 3. MATCHING VALIDATION
            // Check if both password fields are identical
            if (pass1 !== pass2) {
                e.preventDefault();
                showAlert("warning", "Mismatch: The passwords entered do not match. Please re-type them.");
                return;
            }

            // If it passes all checks, the browser will proceed with the POST request
        };
    }
});

/**
 * UI HELPER: Display Bootstrap Alerts
 */
function showAlert(type, message) {
    const alertBox = document.getElementById("alertBox");
    alertBox.innerHTML = `
        <div class="alert alert-${type} alert-dismissible fade show d-flex align-items-center" role="alert">
            <i class="bi bi-exclamation-triangle me-2"></i>
            <div>${message}</div>
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
}

/**
 * UTILITY: Regex Password Validation
 */
function validatePassword(pass) {
    const re = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/;
    return re.test(pass);
}