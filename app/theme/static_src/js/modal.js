document.addEventListener("DOMContentLoaded", () => {
    const genreDropdownButton = document.getElementById("genreDropdownButton");
    const genreDropdown = document.getElementById("genreDropdown");

    // Toggle dropdown visibility
    genreDropdownButton.addEventListener("click", (event) => {
        event.preventDefault();
        genreDropdown.classList.toggle("hidden");
    });

    // Optional: Close dropdown when clicking outside
    window.addEventListener("click", (event) => {
        if (!genreDropdown.contains(event.target) && event.target !== genreDropdownButton) {
            genreDropdown.classList.add("hidden");
        }
    });
});
