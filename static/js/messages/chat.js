let currentConv = null;
let poller = null;

function openChat(convId, username) {
    currentConv = convId;

    // Update header
    document.getElementById("chatHeader").innerText =
        "Chatting with " + username;

    // Enable input
    document.getElementById("msgInput").disabled = false;
    document.getElementById("sendBtn").disabled = false;

    loadMessages();

    if (poller) clearInterval(poller);
    poller = setInterval(loadMessages, 30000);
}


function loadMessages() {
    fetch(`/messages/${currentConv}/`)
        .then(res => res.json())
        .then(data => {
            const box = document.getElementById("chatBox");
            box.innerHTML = "";

            data.messages.forEach(m => {
                const div = document.createElement("div");
                div.className = "msg " + (m.is_me ? "me" : "other");
                div.innerText = m.content;
                box.appendChild(div);
            });

            box.scrollTop = box.scrollHeight;
        });
}

function sendMsg() {
    const input = document.getElementById("msgInput");

    fetch(`/messages/${currentConv}/send/`, {
        method: "POST",
        headers: {
            "X-CSRFToken":
            document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: new URLSearchParams({content: input.value})
    }).then(() => {
        input.value = "";
        loadMessages();
    });
}
