const token = localStorage.getItem("authToken");

document.addEventListener("DOMContentLoaded", async () => {
    try {
        const response = await fetch(dashboardUrl, {
          method: "GET",
          headers: {
              Authorization: `Token ${token}`,
              "X-CSRFToken": csrfToken,
              Accept: "application/json",
            },
            credentials: "include", // Include cookies for session authentication
        });

        if (response.ok) {
            const data = await response.json();
            // Insert the data into the DOM
            document.getElementById("welcome-message").textContent = data.message;

        } else if (response.status === 403) {
            // Handle unauthenticated access
            console.error("User not authenticated. Redirecting to login...");
            window.location.href = "/login/";
        } else {
            console.error("Error fetching dashboard data:", response.statusText);
        }
    } catch (error) {
        console.error("An unexpected error occurred:", error);
    }
});

