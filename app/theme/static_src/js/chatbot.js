document.addEventListener("DOMContentLoaded", () => {
    const chatbotSendButton = document.getElementById("chatbot-send");
    const chatbotInput = document.getElementById("chatbot-input");
    const chatbotMessages = document.getElementById("chatbot-messages");

    chatbotSendButton.addEventListener("click", async () => {
        const userMessage = chatbotInput.value.trim();
        if (!userMessage) return;

        // Display the user's message in the chatbot
        const userMessageDiv = document.createElement("div");
        userMessageDiv.classList.add("chatbot-message", "chatbot-message-user");
        userMessageDiv.innerHTML = `<p>${userMessage}</p>`;
        chatbotMessages.appendChild(userMessageDiv);

        // Clear input
        chatbotInput.value = "";

        // Send the message to the backend
        try {
            const response = await fetch("/api/chatbot/chatbot/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken"),
                },
                body: JSON.stringify({ movie_title: userMessage }),
            });

            const data = await response.json();

            if (response.ok) {
                // Display the bot's response
                const botMessageDiv = document.createElement("div");
                botMessageDiv.classList.add("chatbot-message", "chatbot-message-bot");
                botMessageDiv.innerHTML = `
                    <p><strong>Recommendations:</strong> ${data.content_recommendations.join(", ")}</p>
                    ${
                        data.collaborative_recommendations.length
                            ? `<p><strong>Collaborative:</strong> ${data.collaborative_recommendations.join(", ")}</p>`
                            : ""
                    }
                `;
                chatbotMessages.appendChild(botMessageDiv);
            } else {
                throw new Error(data.error || "An unexpected error occurred.");
            }
        } catch (error) {
            // Display error message
            const errorMessageDiv = document.createElement("div");
            errorMessageDiv.classList.add("chatbot-message", "chatbot-message-error");
            errorMessageDiv.innerHTML = `<p>Error: ${error.message}</p>`;
            chatbotMessages.appendChild(errorMessageDiv);
        }
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
