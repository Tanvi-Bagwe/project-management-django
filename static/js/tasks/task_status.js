/**
 * TASK STATUS UPDATE HANDLER
 * Purpose: Performs an asynchronous PATCH/POST request to update a task's status
 * without refreshing the page. Provides real-time feedback via Bootstrap Modals.
 */

function updateStatus() {
    const statusSelect = document.getElementById("statusSelect");
    const statusModal = document.getElementById("statusModal");
    const updateBtn = document.querySelector("button[onclick='updateStatus()']");

    // 1. DATA RETRIEVAL
    // Extract the dynamic URL from the select element's data attribute
    const targetUrl = statusSelect.getAttribute("data-url");
    const selectedStatus = statusSelect.value;
    const csrfToken = statusSelect.getAttribute("data-csrf");

    // Disable button during request to prevent double-submission
    updateBtn.disabled = true;

    // 2. ASYNC FETCH REQUEST
    fetch(targetUrl, {
        method: "POST",
        headers: {
            "X-CSRFToken": csrfToken,
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Requested-With": "XMLHttpRequest"
        },
        body: new URLSearchParams({
            status_id: selectedStatus
        })
    })
        .then(response => {
            // 3. ERROR HANDLING
            // Check if the server encountered an issue (e.g., database constraint or 404)
            if (!response.ok) {
                return response.json().then(data => {
                    throw new Error(data.message || "Failed to update status.");
                }).catch(() => {
                    throw new Error("Network response was not ok.");
                });
            }
            return response.json();
        })
        .then(data => {
            // 4. UI FEEDBACK
            // On success, trigger the completion modal
            const modalInstance = new bootstrap.Modal(statusModal);
            modalInstance.show();
        })
        .catch(error => {
            // 5. EXCEPTION LOGGING
            console.error("Status Update Error:", error);
            alert("Error updating status: " + error.message);
        })
        .finally(() => {
            // Re-enable button regardless of success or failure
            updateBtn.disabled = false;
        });
}