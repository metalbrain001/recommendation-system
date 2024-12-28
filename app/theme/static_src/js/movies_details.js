document.addEventListener("DOMContentLoaded", async () => {
    const moviePosterContainer = document.getElementById("movie-poster");
    const movieDetailsContainer = document.getElementById("movie-details");
    const movieTrailerContainer = document.getElementById("movie-trailer");

    try {
        const response = await fetch(movieDetailsApiUrl, {
            method: "GET",
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                Accept: "application/json",
            },
        });

        if (!response.ok) {
            throw new Error("Failed to fetch movie details.");
        }

        const data = await response.json();

        // Render poster
        moviePosterContainer.innerHTML = `
            <img src="${data.movie.poster_url}" alt="${data.movie.title}" class="w-full h-auto rounded-md shadow-md">
        `;

        // Render movie details
        movieDetailsContainer.innerHTML = `
            <h1 class="text-4xl font-bold mb-3">${data.movie.title}</h1>
            <p class="text-gray-400">Overview: ${data.movie.overview || "N/A"}</p>
            <p class="text-yellow-400 mt-4">Genres: ${data.movie.genres.map(g => g.name).join(", ") || "N/A"}</p>
            <p class="text-yellow-400">Release Date: ${data.movie.release_date || "N/A"}</p>
            <p class="text-yellow-400">Runtime: ${data.movie.runtime || "N/A"} minutes</p>
            <p class="text-yellow-400">Budget: $${data.movie.budget || "N/A"}</p>
            <p class="text-yellow-400">Rating: ${data.movie.vote_average || "N/A"}/10</p>
        `;

        // Render trailer
        if (data.trailer_url) {
            movieTrailerContainer.innerHTML = `
                <h2 class="text-3xl font-bold">Watch Trailer</h2>
                <iframe class="w-full h-64 md:h-96 rounded-md mt-4" src="${data.trailer_url}" frameborder="0" allowfullscreen></iframe>
            `;
        } else {
            movieTrailerContainer.innerHTML = `
                <p class="text-center text-gray-500 mt-8">Trailer not available for this movie.</p>
            `;
        }
    } catch (error) {
        console.error("Error fetching movie details:", error);
        movieDetailsContainer.innerHTML = `
            <p class="text-red-500">Failed to load movie details. Please try again later.</p>
        `;
    }
});
