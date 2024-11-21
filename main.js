document.getElementById('send-btn').addEventListener('click', sendMessage);
document.getElementById('message-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

function sendMessage() {
    const messageInput = document.getElementById('message-input');
    const messageText = messageInput.value.trim();
    
    if (messageText === "") return;

    // Create a new message element
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', 'user');
    messageElement.textContent = messageText;

    // Append message to the chat box
    const chatBox = document.getElementById('chat-box');
    chatBox.appendChild(messageElement);

    // Scroll to the bottom of the chat box
    chatBox.scrollTop = chatBox.scrollHeight;

    // Clear the input field
    messageInput.value = "";

    // Simulate bot response after 1 second
    setTimeout(function() {
        const botMessageElement = document.createElement('div');
        botMessageElement.classList.add('message', 'bot');
        botMessageElement.textContent = "Bot: " + getBotResponse(messageText);

        chatBox.appendChild(botMessageElement);
        chatBox.scrollTop = chatBox.scrollHeight;
    }, 1000);
}

function getBotResponse(userMessage) {
    // Simple bot response logic, can be extended
    return fetch('http://127.0.0.1:5000/ai', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: userMessage
            })
        })
        .then(response => response.text())
        .catch(error => {
            console.error('Error:', error);
            return 'Sorry, I encountered an error processing your request.';
        }).response;
    
}
