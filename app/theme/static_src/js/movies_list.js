// movies_list.js

// Configuration variables (can be injected dynamically if needed)
const movieListUrl = "/movies_list/"; // API or view endpoint
const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

// Function to load and render the movie list dynamically
export async function loadMovieList(containerId, page = 1) {
    const container = document.getElementById(containerId);

    try {
        const response = await fetch(`${movieListUrl}?page=${page}`, {
            method: "GET",
            headers: {
                "X-CSRFToken": csrfToken,
                "X-Requested-With": "XMLHttpRequest",
            },
        });

        if (response.ok) {
            const html = await response.text();
            container.innerHTML = html; // Insert the response HTML into the container
          attachPaginationListeners(containerId); // Attach pagination click handlers

        } else {
            container.innerHTML = "<p>Failed to load movies. Please try again later.</p>";
            console.error("Error loading movie list:", response.statusText);
        }
    } catch (error) {
        container.innerHTML = "<p>An error occurred. Please try again later.</p>";
        console.error("An unexpected error occurred:", error);
    }
}

// Function to attach pagination click handlers
function attachPaginationListeners(containerId) {
  const container = document.getElementById(containerId);
  const paginationLinks = container.querySelectorAll(".pagination-link");
  console.log("Pagination Links provided",paginationLinks);

    paginationLinks.forEach(link => {
        link.addEventListener("click", function (event) {
            event.preventDefault(); // Prevent full page reload
            const page = new URL(this.href).searchParams.get("page"); // Extract page number
            console.log("Loading page:", page); // Debug log
            loadMovieList(containerId, page); // Load the clicked page dynamically
        });
    });
}
