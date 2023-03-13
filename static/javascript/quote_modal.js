MicroModal.init({
    disableScroll: true,
});

function displayQuoteModal(quoteId) {
    const quoteText = document.getElementById("quote-text-" + quoteId).innerText;
    const quoteAuthor = document.getElementById("quote-author-" + quoteId).innerText;
    const quoteContext = document.getElementById("quote-context-" + quoteId).innerText;
    const userLink = document.getElementById("user-link-" + quoteId).href;
    const userLinkText = document.getElementById("user-link-" + quoteId).innerText;
    const userPic = document.getElementById("user-picture-" + quoteId).src;    
    const likeCount = document.getElementById("quote-like-count-" + quoteId).innerText;
    const datePosted = document.getElementById("quote-date-posted-" + quoteId).innerText;
    const addButton = document.getElementById("quote-add-" + quoteId);
    const isFollowing = document.getElementById("quote-user-" + quoteId).getAttribute("data-following-user");
    const userId = document.getElementById("quote-user-" + quoteId).getAttribute("data-user-id");

    document.getElementById("quote-text-modal").innerText = quoteText;
    document.getElementById("quote-author-modal").innerText = quoteAuthor;
    document.getElementById("quote-context-modal").innerText = quoteContext;
    document.getElementById("user-link-modal").href = userLink;
    document.getElementById("user-link-modal").innerText = userLinkText;
    document.getElementById("user-picture-modal").src = userPic;
    document.getElementById("quote-like-count-modal").innerText = likeCount;
    document.getElementById("quote-date-posted-modal").innerText = datePosted;

    // Add and Remove Buttons
    let modalButton = document.getElementById("quote-add-modal");
    if(addButton.getAttribute("quote-added") === "false") {
        modalButton.querySelector(".quote-footer-buttons-add-label").innerHTML = "Add";
        modalButton.querySelector(".quote-footer-buttons-add-icon").innerHTML = '<i class="fa-solid fa-plus"></i>';
    } else {
        modalButton.querySelector(".quote-footer-buttons-add-label").innerHTML = "Remove";
        modalButton.querySelector(".quote-footer-buttons-add-icon").innerHTML = '<i class="fa-solid fa-check"></i>';
    }
    modalButton.setAttribute("onclick", `addQuote(${quoteId})`);

    // Like Button
    document.getElementById("quote-like-button-modal").setAttribute("onclick", `likeQuote(${quoteId})`);

    // Follow User Button
    const followUserButton = document.getElementById("quote-follow-user-modal");
    if(followUserButton) {
        const loggedInUser = document.getElementById("logged-in-profile").getAttribute("data-user-id");
        if(loggedInUser === userId) {
            followUserButton.style.display = "none";
        } else {
            followUserButton.style.display = "block";
            let userNum = userId.split('|')[1];
            followUserButton.setAttribute("onclick", `followUser(${userNum})`);
            followUserButton.setAttribute("data-following", isFollowing);
            if(isFollowing === "true") {
                followUserButton.querySelector(".quote-footer-buttons-follow-label").innerHTML = "Unfollow User";
                followUserButton.querySelector(".quote-footer-buttons-follow-icon").innerHTML = '<i class="fa-solid fa-check"></i>';
            } else {
                followUserButton.querySelector(".quote-footer-buttons-follow-label").innerHTML = "Follow User";
                followUserButton.querySelector(".quote-footer-buttons-follow-icon").innerHTML = '<i class="fa-solid fa-plus"></i>';
            }
        }
    }

    MicroModal.show("modal-1", {
        disableScroll: true,
    });
}

function displayDeleteModal(quoteId) {
    document.getElementById("delete-modal-button").setAttribute("onclick", "deleteQuote(" + quoteId + ")");
    
    MicroModal.show("delete-quote-modal", {
        disableScroll: true,
    })
}

function displayEditModal(quoteId) {
    document.querySelector(".create-post-modal-title-text").innerHTML = "Edit Post";
    document.querySelector(".create-post-modal-form-submit").innerHTML = "Confirm Edit";

    let quoteText = document.getElementById("quote-text-" + quoteId).innerText;
    let quoteAuthor = document.getElementById("quote-author-" + quoteId).innerText;
    let quoteContext = document.getElementById("quote-context-" + quoteId).innerText;

    let form = document.getElementById("quote-post-form");
    let formText = document.getElementById("form-quote");
    let formAuthor = document.getElementById("form-quote-author");
    let formContext = document.getElementById("form-context");
    let formQuoteId = document.getElementById("form-quote-id");

    formText.value = quoteText;
    formAuthor.value = quoteAuthor;
    formContext.value = quoteContext.trim();
    formQuoteId.value = quoteId;
    form.setAttribute("action", "/edit_post");

    MicroModal.show("create-post-modal", {
        disableScroll: true,
    });
}
