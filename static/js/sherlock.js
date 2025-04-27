document.getElementById('sherlock-form').addEventListener('submit', (e) => {
    e.preventDefault();
    handleFormSubmit('/sherlock/run', 'sherlock-target', 'sherlock-output');
});
