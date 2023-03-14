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
    if(addButton) {
        if(addButton.getAttribute("quote-added") === "false") {
            modalButton.querySelector(".quote-footer-buttons-add-label").innerHTML = "Add";
            modalButton.querySelector(".quote-footer-buttons-add-icon").innerHTML = '<i class="fa-solid fa-plus"></i>';
        } else {
            modalButton.querySelector(".quote-footer-buttons-add-label").innerHTML = "Remove";
            modalButton.querySelector(".quote-footer-buttons-add-icon").innerHTML = '<i class="fa-solid fa-check"></i>';
        }
        modalButton.setAttribute("onclick", `addQuote(${quoteId})`);
    }

    // Like Button
    document.getElementById("quote-like-button-modal").setAttribute("onclick", `likeQuote(${quoteId})`);

    // Follow User Button
    const followUserButton = document.getElementById("quote-follow-user-modal");
    if(followUserButton) {
        followUserButton.style.display = "none";
        const loggedInUser = document.getElementById("logged-in-profile").getAttribute("data-user-id");
        let userNum = userId.split('|')[1];
        if(loggedInUser !== userId) {
            fetch("/api/is-following/" + userNum)
                .then(response => response.json())
                .then(data => {
                    followUserButton.style.display = "block";
                    followUserButton.setAttribute("onclick", "followUser('" + userId + "')");

                    if(data["following"]) {
                        followUserButton.querySelector(".quote-footer-buttons-follow-label").innerHTML = "Unfollow User";
                        followUserButton.querySelector(".quote-footer-buttons-follow-icon").innerHTML = '<i class="fa-solid fa-check"></i>';
                    } else {
                        followUserButton.querySelector(".quote-footer-buttons-follow-label").innerHTML = "Follow User";
                        followUserButton.querySelector(".quote-footer-buttons-follow-icon").innerHTML = '<i class="fa-solid fa-plus"></i>';
                    }
                });
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

    const quoteText = document.getElementById("quote-text-" + quoteId).innerText;
    const quoteAuthor = document.getElementById("quote-author-" + quoteId).innerText;
    const quoteContext = document.getElementById("quote-context-" + quoteId).innerText;

    const form = document.getElementById("quote-post-form");
    const formText = document.getElementById("form-quote");
    const formAuthor = document.getElementById("form-quote-author");
    const formContext = document.getElementById("form-context");
    const formQuoteId = document.getElementById("form-quote-id");

    formText.value = quoteText;
    formAuthor.value = quoteAuthor;
    formContext.value = quoteContext.trim();
    formQuoteId.value = quoteId;
    form.setAttribute("action", "/edit_post");

    MicroModal.show("create-post-modal", {
        disableScroll: true,
    });

    const tagsDiv = document.getElementById("create-post-modal-content").querySelector(".tags");
    tagsDiv.style.display = "none";
    fetch("/api/post-category/" + quoteId)
        .then(response => response.json())
        .then(data => {
            for(let i = 0; i < data.categories.length; i++) {
                let category = data.categories[i];
                let categoryButton = document.getElementById("post-category-" + category);
                if(categoryButton)
                    categoryButton.checked = true;
            }
            tagsDiv.style.display = "flex";
        });
}
