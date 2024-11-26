document.getElementById('openModalButton').addEventListener('click', function () {
    document.getElementById('genreModal').style.display = 'flex';
});

document.getElementById('closeModalButton').addEventListener('click', function () {
    document.getElementById('genreModal').style.display = 'none';
});

document.getElementById('genre').addEventListener('change', function () {
    const selectedGenre = this.value;
    const closeModalButton = document.getElementById('closeModalButton');

    if (selectedGenre) {
        // Update button text and appearance
        closeModalButton.textContent = 'Browse';
        closeModalButton.classList.remove('bg-gray-500', 'hover:bg-gray-700');
        closeModalButton.classList.add('bg-blue-500', 'hover:bg-blue-700');

        // Change button behavior
        closeModalButton.onclick = function () {
            console.log(`Browsing ${selectedGenre} movies...`); // Replace with actual browsing logic
            document.getElementById('genreModal').style.display = 'none';
        };
    }
});

