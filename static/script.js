document.querySelector('.converter-box').addEventListener('submit', function(e) {
    e.preventDefault();

    const urlInput = document.querySelector('input[name="youtube_url"]');
    const formatSelect = document.querySelector('select[name="format_type"]');
    const qualitySelect = document.querySelector('select[name="quality"]');
    const submitBtn = document.querySelector('button[type="submit"]');

    const youtubeUrl = urlInput.value;
    const formatType = formatSelect.value;
    const quality = qualitySelect.value;

    submitBtn.innerText = `Converting to ${formatType.toUpperCase()}... Please wait`;
    submitBtn.style.backgroundColor = "#b30000";
    submitBtn.disabled = true;

    fetch('/convert', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({ 
            'youtube_url': youtubeUrl,
            'format_type': formatType,
            'quality': quality
        })
    })
    .then(response => {
        if (!response.ok) throw new Error('Conversion failed on server.');

        const disposition = response.headers.get('Content-Disposition');
        let filename = `download.${formatType}`; 
        
        if (disposition && disposition.indexOf('attachment') !== -1) {
            const filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
            const matches = filenameRegex.exec(disposition);
            if (matches != null && matches[1]) { 
                filename = matches[1].replace(/['"]/g, '');
            }
        }
        return response.blob().then(blob => ({ blob, filename }));
    })
    .then(({ blob, filename }) => { 
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename; 

        document.body.appendChild(a);
        a.click();
        a.remove();
        
        submitBtn.innerText = "Success! Convert Another?";
        submitBtn.style.backgroundColor = "#28a745";
        submitBtn.disabled = false;
        urlInput.value = ""; 
    })
    .catch(error => {
        console.error('Error:', error);
        alert("Make sure you have FFmpeg installed and the URL is valid!");
        submitBtn.innerText = "Convert Now";
        submitBtn.style.backgroundColor = "#ff0000";
        submitBtn.disabled = false;
    });
});

setInterval(() => {
    fetch('/heartbeat');
}, 5000);