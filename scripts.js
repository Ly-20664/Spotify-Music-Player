document.addEventListener('DOMContentLoaded', function () {
    const toggleButton = document.getElementById('theme-toggle');
    const currentTheme = localStorage.getItem('theme') || 'light-mode';

    // Set the current theme on load
    document.body.classList.add(currentTheme);
    updateComponents(currentTheme);

    // Update the button text based on the current theme
    if (currentTheme === 'dark-mode') {
        toggleButton.textContent = 'Toggle Light Mode';
    } else {
        toggleButton.textContent = 'Toggle Dark Mode';
    }

    // Add an event listener to the toggle button
    toggleButton.addEventListener('click', function () {
        if (document.body.classList.contains('light-mode')) {
            switchToDarkMode();
        } else {
            switchToLightMode();
        }
    });

    function switchToDarkMode() {
        document.body.classList.remove('light-mode');
        document.body.classList.add('dark-mode');
        localStorage.setItem('theme', 'dark-mode');
        toggleButton.textContent = 'Toggle Light Mode';
        updateComponents('dark-mode');
    }

    function switchToLightMode() {
        document.body.classList.remove('dark-mode');
        document.body.classList.add('light-mode');
        localStorage.setItem('theme', 'light-mode');
        toggleButton.textContent = 'Toggle Dark Mode';
        updateComponents('light-mode');
    }

    function updateComponents(theme) {
        const navbar = document.getElementById('navbar');
        const content = document.getElementById('content');
        const audioElements = document.querySelectorAll('audio');

        // Update classes based on the theme
        if (theme === 'dark-mode') {
            applyDarkModeStyles(navbar, content, audioElements);
        } else {
            applyLightModeStyles(navbar, content, audioElements);
        }
    }

    function applyDarkModeStyles(navbar, content, audioElements) {
        navbar.classList.add('navbar-dark-mode');
        navbar.classList.remove('navbar-light-mode');
        content.classList.add('table-dark-mode');
        content.classList.remove('table-light-mode');
        updateButtonsAndInputs('btn-dark-mode', 'input-dark-mode', 'audio-dark-mode', 'playlist-item-dark-mode');
    }

    function applyLightModeStyles(navbar, content, audioElements) {
        navbar.classList.remove('navbar-dark-mode');
        navbar.classList.add('navbar-light-mode');
        content.classList.remove('table-dark-mode');
        content.classList.add('table-light-mode');
        updateButtonsAndInputs('btn-light-mode', 'input-light-mode', 'audio-dark-mode', 'playlist-item-light-mode');
    }

    function updateButtonsAndInputs(btnClass, inputClass, audioClass, playlistItemClass) {
        document.querySelectorAll('button').forEach(button => {
            button.classList.toggle(btnClass);
            button.classList.toggle(btnClass === 'btn-dark-mode' ? 'btn-light-mode' : 'btn-dark-mode');
        });
        document.querySelectorAll('input, textarea').forEach(input => {
            input.classList.toggle(inputClass);
            input.classList.toggle(inputClass === 'input-dark-mode' ? 'input-light-mode' : 'input-dark-mode');
        });
        document.querySelectorAll('audio').forEach(audio => {
            audio.classList.toggle(audioClass);
        });
        document.querySelectorAll('.playlist-item').forEach(item => {
            item.classList.toggle(playlistItemClass);
            item.classList.toggle(playlistItemClass === 'playlist-item-dark-mode' ? 'playlist-item-light-mode' : 'playlist-item-dark-mode');
        });
    }
});
