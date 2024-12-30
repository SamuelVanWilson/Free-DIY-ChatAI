const chatBox = document.getElementById('chat-box');
const inputForm = document.getElementById('input-form');
const userInput = document.getElementById('user-input');

function convertToPreCode(inputText) {
    const regex = /```(.*?)```/gs;
    const result = inputText.replace(regex, (match, p1) => {
        return `<pre><code>${p1}</code></pre>`;
    });
    return result;
}

inputForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const userMessage = userInput.value.trim();
    if (!userMessage) return;

    chatBox.innerHTML += `<div class="user"><strong>You:</strong> ${userMessage}</div>`;
    chatBox.scrollTop = chatBox.scrollHeight;

    userInput.value = '';
    
    chatBox.innerHTML += `<div class="loading"><strong>YourBrandName:</strong><i> Wait a minute, YourBrandName is thinking...</i></div>`;
    chatBox.scrollTop = chatBox.scrollHeight;

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ input: userMessage })
        });
        const result = await response.json();
        const loadingMessage = chatBox.querySelector('.loading');
        if (loadingMessage) {
            loadingMessage.remove();
        }
    
        let outputText =  convertToPreCode(result.output)
        chatBox.innerHTML += `<div class="bot"><strong>YourBrandName:</strong>${outputText}</div>`;

        chatBox.scrollTop = chatBox.scrollHeight;
    } catch (err) {
        const loadingMessage = chatBox.querySelector('.loading');
        if (loadingMessage) {
            loadingMessage.remove();
        }

        chatBox.innerHTML += `<div class="bot"><strong>YourBrandName:</strong>Sorry, an error occurred while contacting the server.</div>`;
        chatBox.scrollTop = chatBox.scrollHeight;
    }
});