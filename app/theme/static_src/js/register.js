 document.getElementById("registrationForm").addEventListener("submit", async function(event) {
            event.preventDefault();

            // Gather form data
            const formData = new FormData(event.target);
            const data = {
                email: formData.get("email"),
                name: formData.get("name"),
                password: formData.get("password")
            };

            // Submit to the API endpoint
            const response = await fetch(registerUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken,
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();
            const messageDiv = document.getElementById("message");

     if (response.status === 201) {
         messageDiv.textContent = "Registration successful!";
         messageDiv.style.color = "green";
         // Redirect to a dashboard or home page after login
         setTimeout(() => {
            window.location.href = redirectUrl; // Use the dynamically defined redirect URL
        }, 2000);

            } else {
                messageDiv.textContent = "Error:" + (result.detail || "Unable to register");
            }
        });