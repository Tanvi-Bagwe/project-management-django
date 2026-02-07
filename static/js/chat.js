/**
 * CORE MESSAGING ENGINE
 * Purpose: This script manages the real-time chat interface.
 * It handles loading message history, sending new messages, and
 * auto-refreshing the chat box so users see new replies.
 */

let currentConv = null; // Stores the active conversation ID
let poller = null;      // Stores the interval timer for refreshing

/**
 * OPEN CHAT
 * Sets up the window for a specific user conversation.
 */
function openChat(convId, username) {
    currentConv = convId;

    // 1. Update UI Header to show who we are talking to
    document.getElementById("chatHeader").innerText = "Chatting with " + username;

    // 2. Enable inputs that were previously disabled
    document.getElementById("msgInput").disabled = false;
    document.getElementById("sendBtn").disabled = false;

    // 3. Initial load of messages
    loadMessages();

    // 4. SETUP POLLING
    // We check for new messages every 5 seconds (5000ms).
    // We clear any existing poller first to avoid "timer stacking".
    if (poller) clearInterval(poller);
    poller = setInterval(loadMessages, 5000);
}

/**
 * LOAD MESSAGES
 * Hits the Django endpoint to get JSON data of all messages in this thread.
 */
function loadMessages() {
    if (!currentConv) return; // Don't run if no chat is selected

    fetch(`/messages/${currentConv}/`)
        .then(res => {
            if (!res.ok) throw new Error("Could not retrieve messages");
            return res.json();
        })
        .then(data => {
            const box = document.getElementById("chatBox");
            box.innerHTML = ""; // Clear current messages to rebuild the list

            // Loop through the messages returned by Django
            data.messages.forEach(m => {
                const div = document.createElement("div");
                // Assignment logic: apply 'me' or 'other' class for CSS bubbles
                div.className = "msg " + (m.is_me ? "me" : "other");
                div.innerText = m.content;
                box.appendChild(div);
            });

            // Auto-scroll to bottom so the newest message is always visible
            box.scrollTop = box.scrollHeight;
        })
        .catch(err => console.error("Polling Error:", err));
}

/**
 * SEND MESSAGE
 * Sends the text input to the database via a POST request.
 */
function sendMsg() {
    const input = document.getElementById("msgInput");
    const messageContent = input.value.trim();

    // Don't send empty messages
    if (!messageContent) return;

    fetch(`/messages/${currentConv}/send/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
            "X-Requested-With": "XMLHttpRequest"
        },
        body: new URLSearchParams({content: messageContent})
    })
        .then(res => {
            if (res.ok) {
                input.value = ""; // Clear input on success
                loadMessages();   // Refresh box immediately
            }
        });
}

/**
 * START NEW CHAT
 * Used by the modal to create a conversation record in the DB.
 */
function startChat() {
    const select = document.getElementById("userSelect");
    const targetUrl = select.getAttribute("data-url");
    const username = select.options[select.selectedIndex].text;

    fetch(targetUrl, {
        method: "POST",
        headers: {
            "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: new URLSearchParams({user_id: select.value})
    })
        .then(res => res.json())
        .then(data => {
            // Switch view to the new chat
            openChat(data.conversation_id, username);

            // Close the Bootstrap Modal
            const modalElement = document.getElementById("newChatModal");
            const modalInstance = bootstrap.Modal.getInstance(modalElement);
            if (modalInstance) modalInstance.hide();
        });
}

// BONUS: Allow sending message by pressing "Enter" key
document.addEventListener('keydown', function (e) {
    if (e.key === "Enter" && document.activeElement.id === "msgInput") {
        sendMsg();
    }
});