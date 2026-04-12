document.querySelector('.converter-box').addEventListener('submit', function(e) {
    e.preventDefault();

    const urlInput = document.querySelector('input[name="youtube_url"]');
    const youtubeUrl = urlInput.value;
    const submitBtn = document.querySelector('button[type="submit"]');

    submitBtn.innerText = "Converting... Please wait";
    submitBtn.style.backgroundColor = "#b30000";
    submitBtn.disabled = true;

    fetch('/convert', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({ 'youtube_url': youtubeUrl })
    })
    .then(response => {
        if (!response.ok) throw new Error('Conversion failed on server.');

        // --- NEW LOGIC: GRABBING THE FILENAME FROM HEADERS ---
        const disposition = response.headers.get('Content-Disposition');
        let filename = "download.mp3"; // Fallback if name is missing
        
        if (disposition && disposition.indexOf('attachment') !== -1) {
            const filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
            const matches = filenameRegex.exec(disposition);
            if (matches != null && matches[1]) { 
                filename = matches[1].replace(/['"]/g, '');
            }
        }
        // We return both the data (blob) and the filename to the next .then()
        return response.blob().then(blob => ({ blob, filename }));
        // ---------------------------------------------------
    })
    .then(({ blob, filename }) => { // Catch both blob and filename
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        
        // --- CHANGED HERE ---
        // Replacing the hardcoded "Aleron_..." name with the variable 'filename'
        a.download = filename; 
        // --------------------

        document.body.appendChild(a);
        a.click();
        a.remove();
        
        submitBtn.innerText = "Success! Convert Another?";
        submitBtn.style.backgroundColor = "#28a745";
        submitBtn.disabled = false;
    
    })
    .catch(error => {
        console.error('Error:', error);
        alert("Make sure you have FFmpeg installed and the URL is valid!");
        submitBtn.innerText = "Convert To MP3";
        submitBtn.style.backgroundColor = "#ff0000";
        submitBtn.disabled = false;
    });
});