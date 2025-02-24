function sendMessage() {
    let userInput = document.getElementById("user-input").value;
    if (!userInput) return;

    let chatBox = document.getElementById("chat-box");
    chatBox.innerHTML += `<p><strong>You:</strong> ${userInput}</p>`;

    fetch('/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userInput })
    })
    .then(response => response.json())
    .then(data => {
        chatBox.innerHTML += `
            <div class="bot-response">
                <img src="/static/images/fitness_trainer.png" alt="Fitness Trainer" class="trainer-image">
                <p><strong>NutriByte trainer:</strong> ${data.reply}</p>
            </div>
        `;
        document.getElementById("user-input").value = "";
        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(error => console.error("Error:", error));
}