MicroModal.init({
    disableScroll: true,
});

function displayQuoteModal(quoteId) {
    let quoteText = document.getElementById("quote-text-" + quoteId).innerText;
    let quoteAuthor = document.getElementById("quote-author-" + quoteId).innerText;
    let quoteContext = document.getElementById("quote-context-" + quoteId).innerText;
    let userLink = document.getElementById("user-link-" + quoteId).href;
    let userLinkText = document.getElementById("user-link-" + quoteId).innerText;
    let userPic = document.getElementById("user-picture-" + quoteId).src;    
    let likeCount = document.getElementById("quote-like-count-" + quoteId).innerText;
    let datePosted = document.getElementById("quote-date-posted-" + quoteId).innerText;
    let addButton = document.getElementById("quote-add-" + quoteId);
    let removeButton = document.getElementById("quote-remove-" + quoteId);

    document.getElementById("quote-text-modal").innerText = quoteText;
    document.getElementById("quote-author-modal").innerText = quoteAuthor;
    document.getElementById("quote-context-modal").innerText = quoteContext;
    document.getElementById("user-link-modal").href = userLink;
    document.getElementById("user-link-modal").innerText = userLinkText;
    document.getElementById("user-picture-modal").src = userPic;
    document.getElementById("quote-like-count-modal").innerText = likeCount;
    document.getElementById("quote-date-posted-modal").innerText = datePosted;

    // Buttons
    if(addButton) {
        if(addButton.style.display === "none") {
            document.getElementById("quote-add-modal").style.display = "none";
            document.getElementById("quote-remove-modal").style.display = "block";
            document.getElementById("quote-remove-modal").setAttribute("onclick", "removeQuote(" + quoteId + ")");
        } else {
            document.getElementById("quote-add-modal").style.display = "block";
            document.getElementById("quote-remove-modal").style.display = "none";
            document.getElementById("quote-add-modal").setAttribute("onclick", "addQuote(" + quoteId + ")");
        }
    }
    document.getElementById("quote-like-button-modal").setAttribute("onclick", "likeQuote(" + quoteId + ")");

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
