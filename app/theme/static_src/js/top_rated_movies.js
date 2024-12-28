const topRatedMovies = "/top_rated_movies/"; // API endpoint for top-rated movies
const token = localStorage.getItem("authToken");

document.addEventListener("DOMContentLoaded", async () => {
    const topRatedMoviesContainer = document.getElementById("top_rated_movies");

    try {
        // Fetch top-rated movies
        const response = await fetch(topRatedMovies, {
            method: "GET",
            headers: {
                Authorization: `Token ${token}`,
                "X-CSRFToken": csrfToken,
                 Accept: "application/json",
                "X-Requested-With": "XMLHttpRequest", // Add this header
            },
            credentials: "include", // Include cookies for session authentication
        });

        if (response.ok) {
            const movies = await response.json();
            renderMovies(movies, topRatedMoviesContainer);
        } else {
            topRatedMoviesContainer.innerHTML = "<p class='text-red-500'>Failed to load top-rated movies.</p>";
            console.error("Error fetching top-rated movies:", response.statusText);
        }
    } catch (error) {
        topRatedMoviesContainer.innerHTML = "<p class='text-red-500'>An error occurred. Please try again later.</p>";
        console.error("An unexpected error occurred:", error);
    }
});

function createMovieElement(movie) {
    const movieElement = document.createElement("div");
    movieElement.className = "flex flex-col items-center bg-slate-900 p-4 rounded-lg shadow-lg w-48";

    movieElement.innerHTML = `
        <a href="/movies_details/${movie.movie_id}/">
            <div class="relative w-48 h-[calc(3/2*12rem)] rounded-md overflow-hidden">
                <img src="${movie.poster_url || "https://via.placeholder.com/150"}"
                     alt="${movie.title}" class="w-full h-full object-cover">
            </div>
        </a>
        <h3 class="text-md font-semibold text-center mt-2">${movie.title}</h3>
        <p class="text-center text-yellow-400">
            Rating: ${movie.average_rating || "N/A"} / 5.0
        </p>
    `;

    return movieElement;
}



function renderMovies(movies, container) {
    if (movies.length === 0) {
        container.innerHTML = "<p class='text-gray-300 text-center'>No top-rated movies found.</p>";
        return;
    }

    const fragment = document.createDocumentFragment();
    movies.slice(0, 12).forEach((movie) => {
        const movieElement = createMovieElement(movie);
        fragment.appendChild(movieElement);
    });

    container.innerHTML = ""; // Clear previous content
    container.appendChild(fragment); // Append new movie elements
}


