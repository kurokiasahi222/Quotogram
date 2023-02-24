async function apiRequest(quote_id, request) {
    const response = await fetch(request, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            quote_id: quote_id
        })
    }).then(response => {
        if(response.status !== 200) {
            throw new Error("Error while performing request");
        }

        const data = response.json();
        return data;
    });
}

function likeQuote(quote_id) {
    apiRequest(quote_id, 'api/like')
        .then(data => {
            const likeCountSpan = document.getElementById(`quote-like-count-${quote_id}`);
            likeCountSpan.innerHTML = data.num_likes;

            // In case modal is active we set the likes for modal as well
            const modalLikeCountSpan = document.getElementById("quote-like-count-modal");
            modalLikeCountSpan.innerHTML = data.num_likes;
        })
        .catch(error => {
            console.error(error);
        });
}

function addQuote(quote_id) {
    apiRequest(quote_id, '/api/follow/post')
        .then(data => {
            const addQuoteButton = document.getElementById(`quote-add-${quote_id}`);
            const removeQuoteButton = document.getElementById(`quote-remove-${quote_id}`);

            addQuoteButton.style.display = "none";
            removeQuoteButton.style.display = "block";
        })
        .catch(error => {
            console.error(error);
        });
}

function removeQuote(quote_id) {
    apiRequest(quote_id, '/api/follow/post')
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

function deleteQuote(quote_id) {
    apiRequest(quote_id, 'api/delete')
        .then(data => {
            if(data.successful) {
                // TODO: perform a page reload
            }
        })
        .catch(error => {
            console.error(error);
        });
}
