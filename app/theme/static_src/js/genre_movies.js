document.addEventListener("DOMContentLoaded", () => {
    loadGenreMovies(); // Load the first page of movies
});

async function loadGenreMovies(page = 1) {
    const urlParts = window.location.pathname.split('/');
    const genre = urlParts[urlParts.length - 2]; // Extract genre from URL
    const genreUrl = `/genre_movies_full_page/${genre}/?page=${page}`; // Construct API endpoint
    const container = document.querySelector(".movie-grid"); // Grid container for movies
    const paginationContainer = document.querySelector(".pagination-container"); // Pagination container
    const csrfToken = "{{ csrf_token }}"; // CSRF token

    try {
        const response = await fetch(genreUrl, {
            method: "GET",
            headers: {
                "X-CSRFToken": csrfToken,
                Accept: "application/json",
                "X-Requested-With": "XMLHttpRequest",
            },
        });

        if (response.ok) {
            const data = await response.json();
            renderMovies(data.movies, container); // Render movies
            renderPagination(data.page, data.total_pages, paginationContainer); // Render pagination links
        } else {
            container.innerHTML = `<p class='text-red-500'>Failed to load movies for this genre.</p>`;
        }
    } catch (error) {
        container.innerHTML = `<p class='text-red-500'>An error occurred. Please try again later.</p>`;
        console.error(`Error fetching movies for page ${page}:`, error);
    }
}

function renderMovies(movies, container) {
    container.innerHTML = ""; // Clear previous content
    const fragment = document.createDocumentFragment();

    movies.forEach((movie) => {
        const movieElement = document.createElement("div");
        movieElement.className = "flex flex-col items-center bg-slate-900 p-4 rounded-lg shadow-lg";
        movieElement.innerHTML = `
            <a href="/movies_details/${movie.movie_id}/">
                <div class="relative w-48 h-[calc(3/2*12rem)] rounded-md overflow-hidden">
                    <img src="${movie.poster_url || "https://via.placeholder.com/500x750?text=No+Poster"}"
                         alt="${movie.title}" class="w-full h-full object-cover">
                </div>
            </a>
            <h3 class="text-md font-semibold text-center mt-2">${movie.title}</h3>
            <p class="text-center text-yellow-400">Rating: ${movie.average_rating || "N/A"}</p>
        `;
        fragment.appendChild(movieElement);
    });

    container.appendChild(fragment); // Add movies to container
}

function renderPagination(currentPage, totalPages, container) {
    container.innerHTML = ""; // Clear previous content

    if (currentPage > 1) {
        container.innerHTML += `<a href="#" data-page="1" class="pagination-link mx-2 px-4 py-2 bg-blue-600 text-white rounded-md">First</a>`;
        container.innerHTML += `<a href="#" data-page="${currentPage - 1}" class="pagination-link mx-2 px-4 py-2 bg-blue-600 text-white rounded-md">Previous</a>`;
    }

    container.innerHTML += `<span class="mx-2 px-4 py-2 bg-gray-500 text-white rounded-md">Page ${currentPage} of ${totalPages}</span>`;

    if (currentPage < totalPages) {
        container.innerHTML += `<a href="#" data-page="${currentPage + 1}" class="pagination-link mx-2 px-4 py-2 bg-blue-600 text-white rounded-md">Next</a>`;
        container.innerHTML += `<a href="#" data-page="${totalPages}" class="pagination-link mx-2 px-4 py-2 bg-blue-600 text-white rounded-md">Last</a>`;
    }

    // Attach event listeners to pagination links
    const paginationLinks = container.querySelectorAll(".pagination-link");
    paginationLinks.forEach((link) => {
        link.addEventListener("click", (event) => {
            event.preventDefault(); // Prevent default link behavior
            const page = link.getAttribute("data-page");
            loadGenreMovies(page); // Load the corresponding page
        });
    });
}
