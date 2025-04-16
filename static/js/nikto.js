document.getElementById('nikto-form').addEventListener('submit', async (e) => {
    e.preventDefault(); // Empêche la soumission du formulaire par défaut
    const host = document.getElementById('nikto-host').value;
    const options = document.getElementById('nikto-options').value;
    const output = document.getElementById('nikto-output');

    output.textContent = 'Running Nikto...';

    try {
        const response = await fetch('/nikto/run', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ host, options })
        });

        if (response.ok) {
            const data = await response.json();
            output.textContent = data.output;
        } else {
            const errorData = await response.json();
            output.textContent = `Error: ${errorData.error || response.statusText}`;
        }
    } catch (error) {
        output.textContent = `Error: ${error.message}`;
    }
});