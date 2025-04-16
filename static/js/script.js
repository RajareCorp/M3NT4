async function handleFormSubmit(endpoint, targetFieldId, outputId) {
    const target = document.getElementById(targetFieldId).value;
    const output = document.getElementById(outputId);
    output.textContent = 'Loading...';

    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ target })
        });

        if (response.ok) {
            const data = await response.json();
            output.textContent = data.output;
        } else {
            output.textContent = `Error: ${response.statusText}`;
        }
    } catch (error) {
        output.textContent = `Error: ${error.message}`;
    }
}

async function loadPublicIP() {
    const ipElement = document.getElementById('public-ip');
    try {
        const response = await fetch('/ifconfig');
        if (response.ok) {
            const data = await response.json();
            ipElement.textContent = data.output;
        } else {
            ipElement.textContent = 'Error fetching IP';
        }
    } catch (error) {
        ipElement.textContent = `Error: ${error.message}`;
    }
}

// Charger l'IP publique dès que la page est prête
document.addEventListener('DOMContentLoaded', loadPublicIP);
