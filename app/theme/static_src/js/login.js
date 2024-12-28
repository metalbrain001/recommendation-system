document.getElementById("loginForm").addEventListener("submit", async function(event) {
    event.preventDefault();

    // Gather form data
    const formData = new FormData(event.target);

    try {
        // Send POST request
        const response = await fetch(loginUrl, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrfToken, // Include CSRF token
                "X-Requested-With": "XMLHttpRequest", // Mark as AJAX
            },
            body: formData, // Use FormData for compatibility with Django's request.POST
        });

        const contentType = response.headers.get("Content-Type");
        if (contentType && contentType.includes("application/json")) {
            const result = await response.json();
            if (response.ok) {
                // Handle success
                document.getElementById("message").textContent = result.message || "Login successful!";
                window.location.href = result.redirect_url || redirectUrl;
            } else {
                // Handle error
                document.getElementById("message").textContent = result.error || "Invalid login credentials";
            }
        } else {
            // Handle unexpected HTML response
            const html = await response.text();
            console.error("Unexpected HTML response:", html);
            document.getElementById("message").textContent = "An unexpected error occurred.";
        }
    } catch (error) {
        console.error("An unexpected error occurred:", error);
        document.getElementById("message").textContent = "An unexpected error occurred. Please try again.";
    }
});
