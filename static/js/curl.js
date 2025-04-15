document.getElementById('curl-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const url = document.getElementById('curl-url').value;
    const outputElement = document.getElementById('curl-output');

    outputElement.textContent = 'Fetching...';

    try {
        const response = await fetch('/curl', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url }),
        });

        if (response.ok) {
            const data = await response.json();
            outputElement.textContent = data.output;
        } else {
            const errorData = await response.json();
            outputElement.textContent = `Error: ${errorData.error}`;
        }
    } catch (error) {
        outputElement.textContent = `Error: ${error.message}`;
    }
});
