document.addEventListener("DOMContentLoaded", () => {
    const userMenuButton = document.getElementById("user-menu-button");
    const userMenu = document.getElementById("user-menu");

    // Toggle dropdown visibility
    userMenuButton.addEventListener("click", () => {
        userMenu.classList.toggle("hidden");
    });

    // Hide dropdown if clicking outside
    document.addEventListener("click", (event) => {
        if (!userMenu.contains(event.target) && !userMenuButton.contains(event.target)) {
            userMenu.classList.add("hidden");
        }
    });
});
