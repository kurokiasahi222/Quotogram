async function apiRequest(quote_id, request) {
    const response = await fetch(request, {
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
    apiRequest(quote_id, 'api/like')
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

function addQuote(quote_id) {
    apiRequest(quote_id, 'api/add')
        .then(data => {
            if(data.successful) {
                const addQuoteButton = document.getElementById(`quote-add-${quote_id}`);
                const removeQuoteButton = document.getElementById(`quote-remove-${quote_id}`);

                addQuoteButton.style.display = "none";
                removeQuoteButton.style.display = "block";
            }
        })
        .catch(error => {
            console.error(error);
        });
}

function removeQuote(quote_id) {
    apiRequest(quote_id, 'api/remove')
        .then(data => {
            const addQuoteButton = document.getElementById(`quote-add-${quote_id}`);
            const removeQuoteButton = document.getElementById(`quote-remove-${quote_id}`);

            addQuoteButton.style.display = "block";
            removeQuoteButton.style.display = "none";
        })
        .catch(error => {
            console.error(error);
        });
}
