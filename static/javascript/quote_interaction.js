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

    console.log("Response status: " + response.status);
    if(response.status !== 200) {
        throw new Error("Error: " + response.status);
    }

    let result = response.json();
    console.log("Data: " + result);
    return result;
}

function likeQuote(quote_id) {
    apiRequest(quote_id, 'api/like')
        .then(data => {
            console.log("Finished liking the quote, here is the call back data: " + data);

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

function deleteQuote(quote_id) {
    apiRequest(quote_id, 'api/delete')
        .then(data => {
            if(data.status === 'success') {
                location.reload();
            }
        })
        .catch(error => {
            console.error(error);
        });
}

let openDropdown = null;

function toggleEditOptions(quote_id) {
    if(openDropdown) {
        const editOptions = document.getElementById(`quote-dropdown-content-${openDropdown}`);
        editOptions.style.display = "none";
    }
    
    const editOptions = document.getElementById(`quote-dropdown-content-${quote_id}`);
    editOptions.style.display = "block";
    openDropdown = quote_id;

    let bounding = editOptions.getBoundingClientRect();
    if(bounding.bottom > (window.innerHeight || document.documentElement.clientHeight)) {
        editOptions.style.top = "-1em";
    }
}

document.addEventListener('click', function(event) {
    if(openDropdown !== null && !event.target.matches(`#quote-dropdown-${openDropdown}`) && !event.target.matches('.quote-footer-buttons-dropdown')) {
        const editOptions = document.getElementById(`quote-dropdown-content-${openDropdown}`);
        editOptions.style.display = "none";
        openDropdown = null;
    }
});
