document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("registerForm");
    const submitBtn = document.getElementById("submitBtn");

    // MAIN TRIGGER: This invokes everything
    form.addEventListener("submit", function (e) {
        e.preventDefault(); // Stop page refresh
        processRegistration();
    });

    function processRegistration() {
        const alertBox = document.getElementById("alertBox");
        alertBox.innerHTML = ""; // Clear old alerts

        // Execute individual validations
        const errorMessage = runValidationChecks();

        if (errorMessage) {
            showAlert("danger", errorMessage);
        } else {
            // If all checks pass, call the submission method
            sendDataToServer();
        }
    }

    // --- VALIDATION SUITE ---
    function runValidationChecks() {
        const fName = form["first_name"].value.trim();
        const lName = form["last_name"].value.trim();
        const user = form["username"].value.trim();
        const email = form["email"].value.trim();
        const pass = form["password"].value.trim();

        // First Name Validation
        if (fName === "") {
            return "First name is required.";
        } else if (fName.length < 2) {
            return "First name must be at least 2 characters.";
        }

        // Last Name Validation
        if (lName === "") {
            return "Last name is required.";
        } else if (lName.length < 2) {
            return "Last name must be at least 2 characters.";
        }

        // Username Pattern Validation
        if (!validateUsername(user)) {
            return "Username must be 5-12 characters (letters and numbers only).";
        }

        // Email Pattern Validation
        if (!validateEmail(email)) {
            return "Please provide a valid email address.";
        }

        // Password Pattern Validation
        if (!validatePassword(pass)) {
            return "Password must be at least 8 characters and include 1 letter and 1 number.";
        }

        return null; // All good!
    }

    // --- HELPER METHODS (Patterns) ---

    function validateUsername(username) {
        const re = /^[a-zA-Z0-9]{5,12}$/;
        return re.test(username);
    }

    function validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }

    function validatePassword(pass) {
        // Minimum eight characters, at least one letter and one number
        const re = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/;
        return re.test(pass);
    }

    // --- AJAX SUBMISSION ---

    function sendDataToServer() {
        submitBtn.disabled = true;
        submitBtn.innerHTML = `<span class="spinner-border spinner-border-sm"></span> Processing...`;

        const formData = new FormData(form);

        fetch(form.dataset.submitUrl, {
            method: "POST",
            body: formData,
            // Django requires the CSRF token in the header for AJAX
            headers: {
                "X-CSRFToken": form.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
            .then(res => res.json())
            .then(data => {
                resetButton();
                if (data.success) {
                    showAlert("success", data.message);
                    form.reset();
                } else {
                    showAlert("danger", data.message);
                }
            })
            .catch(() => {
                resetButton();
                showAlert("danger", "An error occurred. Please try again.");
            });
    }

    function resetButton() {
        submitBtn.disabled = false;
        submitBtn.innerHTML = "Register";
    }

    function showAlert(type, message) {
        const alertBox = document.getElementById("alertBox");
        alertBox.innerHTML = `
            <div class="alert alert-${type} alert-dismissible fade show">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
    }
});