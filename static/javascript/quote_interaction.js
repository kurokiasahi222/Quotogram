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
    const likeCountSpan = document.getElementById(`quote-like-count-${quote_id}`);
    const modalLikeCountSpan = document.getElementById("quote-like-count-modal");

    likeCountSpan.innerHTML = '<i class="fa-solid fa-spinner"></i>';
    modalLikeCountSpan.innerHTML = likeCountSpan.innerHTML;

    likeCountSpan.classList.toggle("spin");
    modalLikeCountSpan.classList.toggle("spin");

    apiRequest(quote_id, 'api/like')
        .then(data => {
            console.log("Finished liking the quote, here is the call back data: " + data);
            likeCountSpan.innerHTML = data.num_likes;
            modalLikeCountSpan.innerHTML = data.num_likes;

            likeCountSpan.classList.toggle("spin");
            modalLikeCountSpan.classList.toggle("spin");
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
            if(data.status === 'success') {
                location.reload();
            }
        })
        .catch(error => {
            console.error(error);
        });
}

let openWrapper = null;
let openDropdown = null;

function toggleEditOptions(quote_id) {
    let wrapper = document.querySelector(".quote-wrapper[data-quote-id='" + quote_id + "']");
    wrapper.style.zIndex = 1;

    if(openDropdown) {
        const editOptions = document.getElementById(`quote-dropdown-content-${openDropdown}`);
        editOptions.style.display = "none";
        openWrapper.style.zIndex = 0;
    }
    
    const editOptions = document.getElementById(`quote-dropdown-content-${quote_id}`);
    editOptions.style.display = "block";
    openDropdown = quote_id;
    openWrapper = wrapper;

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
        openWrapper.style.zIndex = 0;
    }
});
