document.getElementById('photon-form').addEventListener('submit', (e) => {
    e.preventDefault();
    handleFormSubmit('/photon/run', 'photon-target', 'photon-output');
});

document.getElementById('load-photon-results').addEventListener('click', async () => {
    const resultsList = document.getElementById('photon-results-list');
    const resultContent = document.getElementById('photon-result-content');
    resultsList.innerHTML = '';
    resultContent.textContent = '';

    try {
        const response = await fetch('/photon/results');
        if (response.ok) {
            const data = await response.json();
            if (data.files && data.files.length > 0) {
                data.files.forEach(file => {
                    const listItem = document.createElement('li');
                    const link = document.createElement('a');
                    link.href = `#`;
                    link.textContent = file;
                    link.addEventListener('click', (e) => {
                        e.preventDefault();
                        loadPhotonResult(file);
                    });
                    listItem.appendChild(link);
                    resultsList.appendChild(listItem);
                });
            } else {
                resultsList.innerHTML = '<li>No results available</li>';
            }
        } else {
            resultsList.innerHTML = `<li>Error: ${response.statusText}</li>`;
        }
    } catch (error) {
        resultsList.innerHTML = `<li>Error: ${error.message}</li>`;
    }
});

async function loadPhotonResult(filename) {
    const resultContent = document.getElementById('photon-result-content');
    resultContent.textContent = 'Loading...';

    try {
        const response = await fetch(`/photon/results/${filename}`);
        if (response.ok) {
            const data = await response.text();
            resultContent.textContent = data;
        } else {
            resultContent.textContent = `Error: ${response.statusText}`;
        }
    } catch (error) {
        resultContent.textContent = `Error: ${error.message}`;
    }
}