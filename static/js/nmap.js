document.getElementById('nmap-form').addEventListener('submit', (e) => {
    e.preventDefault();
    handleFormSubmit('/nmap/run', 'nmap-target', 'nmap-output');
});
