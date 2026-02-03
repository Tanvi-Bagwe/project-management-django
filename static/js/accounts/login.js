document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("loginForm");
    const submitBtn = document.getElementById("submitBtn");

    form.addEventListener("submit", function (e) {
        e.preventDefault();
        processLogin();
    });

    function processLogin() {
        const alertBox = document.getElementById("alertBox");
        alertBox.innerHTML = "";

        const username = form["username"].value.trim();
        const password = form["password"].value.trim();

        if (username === "" || password === "") {
            showAlert("danger", "Username and password are required.");
            return;
        }

        submitBtn.disabled = true;
        submitBtn.innerHTML =
            `<span class="spinner-border spinner-border-sm"></span> Logging in...`;

        const formData = new FormData(form);

        fetch(form.dataset.submitUrl, {
            method: "POST",
            body: formData,
            headers: {
                "X-CSRFToken": form.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
            .then(res => res.json())
            .then(data => {
                resetButton();
                if (data.success) {
                    showAlert("success", data.message);
                    setTimeout(() => {
                        window.location.href = data.redirect_url;
                    }, 1000);
                } else {
                    showAlert("danger", data.message);
                }
            })
            .catch(() => {
                resetButton();
                showAlert("danger", "Login failed. Try again.");
            });
    }

    function resetButton() {
        submitBtn.disabled = false;
        submitBtn.innerHTML = "Login";
    }

    function showAlert(type, message) {
        document.getElementById("alertBox").innerHTML = `
            <div class="alert alert-${type} alert-dismissible fade show">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
    }
});
