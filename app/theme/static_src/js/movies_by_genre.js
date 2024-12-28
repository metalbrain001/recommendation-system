document.addEventListener("DOMContentLoaded", async () => {
    const genres = ["action", "romance", "documentary"]; // Define genres for the dashboard
    const csrfToken = "{{ csrf_token }}"; // Ensure CSRF token is available

    genres.forEach(async (genre) => {
        const container = document.getElementById(`${genre}_movies`);
        const genreUrl = `/movies_by_genre/${genre}/`; // Dynamically construct URL for each genre

        try {
            const response = await fetch(genreUrl, {
                method: "GET",
                headers: {
                    "X-CSRFToken": csrfToken,
                    Accept: "application/json",
                    "X-Requested-With": "XMLHttpRequest",
                },
                credentials: "include",
            });

            if (response.ok) {
                const movies = await response.json();
                renderMovies(movies, container);
            } else {
                container.innerHTML = `<p class='text-red-500'>Failed to load ${genre} movies.</p>`;
            }
        } catch (error) {
            container.innerHTML = `<p class='text-red-500'>An error occurred while loading ${genre} movies.</p>`;
            console.error(`Error fetching ${genre} movies:`, error);
        }
    });
});

function renderMovies(movies, container) {
    container.innerHTML = ""; // Clear previous content
    const fragment = document.createDocumentFragment();

    movies.forEach((movie) => {
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
        fragment.appendChild(movieElement);
    });

    container.appendChild(fragment); // Add movies to container
}
