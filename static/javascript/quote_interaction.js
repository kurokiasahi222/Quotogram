async function likeRequest(quote_id) {
    const response = await fetch('/api/like', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            quote_id: quote_id
        })
    });
    const data = await response.json();

    if(!data.ok) {
        const message = `Error: ${data.error}`;
        throw new Error(message);
    }

    return data;
}

function likeQuote(quote_id) {
    likeRequest(quote_id)
        .then(data => {
            const likeCountSpan = document.getElementById(`quote-like-count-${quote_id}`);
            likeCountSpan.innerHTML = data.likes;

            // In case modal is active we set the likes for modal as well
            const modalLikeCountSpan = document.getElementById("quote-like-count-modal");
            modalLikeCountSpan.innerHTML = data.likes;
        })
        .catch(error => {
            console.error(error);
        });
}