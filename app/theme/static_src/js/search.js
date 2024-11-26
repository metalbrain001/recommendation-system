
    document.getElementById('movieSearchInput').addEventListener('input', function () {
        const query = this.value.trim();
        const searchResults = document.getElementById('searchResults');

        // Clear previous results if query is empty
        if (!query) {
            searchResults.innerHTML = '';
            searchResults.classList.add('hidden');
            return;
        }

        // Perform AJAX request to fetch matching movies
        fetch(`/real-time-search/?query=${encodeURIComponent(query)}`, {
            headers: {
                'x-requested-with': 'XMLHttpRequest', // Indicates AJAX request
            },
        })
            .then((response) => response.json())
            .then((movies) => {
                searchResults.innerHTML = ''; // Clear old results
                if (movies.length > 0) {
                    searchResults.classList.remove('hidden');
                    movies.forEach((movie) => {
                        const li = document.createElement('li');
                        li.textContent = movie.title;
                      li.classList.add('px-4', 'py-2', 'hover:bg-gray-800', 'cursor-pointer');

                      // Add movie posters to search results
                      const img = document.createElement('img');
                      img.src = movie.poster_url || '/static/default-poster.jpg';
                      img.alt = `${movie.title} poster`;
                      img.classList.add('w-16', 'h-16', 'object-cover', 'rounded', 'mr-4');
                      // Append elements to the list item
                      li.appendChild(img);

                        li.addEventListener('click', () => {
                            document.getElementById('movieSearchInput').value = movie.title;
                            searchResults.innerHTML = '';
                            searchResults.classList.add('hidden');
                        });
                        searchResults.appendChild(li);
                    });
                } else {
                    searchResults.innerHTML = '<li class="px-4 py-2 text-gray-500">No results found</li>';
                    searchResults.classList.remove('hidden');
                }
            })
            .catch((error) => {
                console.error('Error fetching movies:', error);
                searchResults.innerHTML = '<li class="px-4 py-2 text-red-500">Error loading results</li>';
                searchResults.classList.remove('hidden');
            });
    });
