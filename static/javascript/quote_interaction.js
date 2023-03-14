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

    // console.log("Response status: " + response.status);
    if(response.status !== 200) {
        throw new Error("Error: " + response.status);
    }

    let result = response.json();
    // console.log("Data: " + result);
    return result;
}

function likeQuote(quote_id) {
    if(!canInteract())
        return;

    const likeCountSpan = document.getElementById(`quote-like-count-${quote_id}`);
    const modalLikeCountSpan = document.getElementById("quote-like-count-modal");

    likeCountSpan.innerHTML = '<i class="fa-solid fa-spinner"></i>';
    modalLikeCountSpan.innerHTML = likeCountSpan.innerHTML;

    likeCountSpan.classList.toggle("spin");
    modalLikeCountSpan.classList.toggle("spin");

    apiRequest(quote_id, 'api/like')
        .then(data => {
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
    if(!canInteract())
        return;

    const quoteButton = document.getElementById(`quote-add-${quote_id}`);
    const quoteButtonIcon = quoteButton.querySelector(".quote-footer-buttons-add-icon");
    let status = quoteButton.getAttribute("quote-added");

    const quoteButtonModal = document.getElementById("quote-add-modal");
    const quoteButtonIconModal = quoteButtonModal.querySelector(".quote-footer-buttons-add-icon");
    
    let initalVaue = quoteButtonIcon.innerHTML;
    quoteButtonIcon.innerHTML = '<i class="fa-solid fa-spinner"></i>';
    quoteButtonIconModal.innerHTML = quoteButtonIcon.innerHTML;

    quoteButtonIcon.classList.toggle("spin");
    quoteButtonIconModal.classList.toggle("spin");

    apiRequest(quote_id, '/api/follow/post')
        .then(data => {
            if(data.status === 'failed') {
                quoteButtonIcon.innerHTML = initalVaue;
                quoteButtonIcon.classList.toggle("spin");
                quoteButtonIconModal.classList.toggle("spin");
                return;
            }
            if(status === 'true') { // The quote was added, so now show that it was removed
                quoteButton.setAttribute("quote-added", "false");

                quoteButton.querySelector(".quote-footer-buttons-add-label").innerHTML = "Add";
                quoteButtonModal.querySelector(".quote-footer-buttons-add-label").innerHTML = "Add";

                quoteButtonIcon.innerHTML = '<i class="fa-solid fa-plus"></i>';
                quoteButtonIconModal.innerHTML = quoteButtonIcon.innerHTML;
            } else {
                quoteButton.setAttribute("quote-added", "true");

                quoteButton.querySelector(".quote-footer-buttons-add-label").innerHTML = "Remove";
                quoteButtonModal.querySelector(".quote-footer-buttons-add-label").innerHTML = "Remove";

                quoteButtonIcon.innerHTML = '<i class="fa-solid fa-check"></i>';
                quoteButtonIconModal.innerHTML = quoteButtonIcon.innerHTML;
            }

            quoteButtonIcon.classList.toggle("spin");
            quoteButtonIconModal.classList.toggle("spin");
        })
        .catch(error => {
            console.error(error);
        });
}

function deleteQuote(quote_id) {
    if(!canInteract())
        return;

    apiRequest(quote_id, '/api/delete')
        .then(data => {
            if(data.status === 'success') {
                location.reload();
            }
        })
        .catch(error => {
            console.error(error);
        });
}

function followUser(user_id) {
    if(!canInteract())
        return;

    const followUserButton = document.getElementById("quote-follow-user-modal");
    const followUserButtonLabel = followUserButton.querySelector(".quote-footer-buttons-follow-label");
    const followUserButtonIcon = followUserButton.querySelector(".quote-footer-buttons-follow-icon");
    let following = followUserButton.getAttribute("data-following");

    followUserButtonIcon.innerHTML = '<i class="fa-solid fa-spinner"></i>';
    followUserButtonIcon.classList.toggle("spin");

    apiRequest(user_id, 'api/follow/user')
        .then(data => {
            if(following === 'true') { // user has unfollowed the user
                followUserButton.setAttribute("data-following", false);
                followUserButtonLabel.innerHTML = "Follow User";
                followUserButtonIcon.innerHTML = '<i class="fa-solid fa-plus"></i>';
            } else {
                followUserButton.setAttribute("data-following", true);
                followUserButtonLabel.innerHTML = "Unfollow User";
                followUserButtonIcon.innerHTML = '<i class="fa-solid fa-check"></i>';
            }
            followUserButtonIcon.classList.toggle("spin");
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

function canInteract() {
    return document.querySelector("body").getAttribute("data-can-interact") === "true";
}
