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

    document.getElementById("quote-text-modal").innerText = quoteText;
    document.getElementById("quote-author-modal").innerText = quoteAuthor;
    document.getElementById("quote-context-modal").innerText = quoteContext;
    document.getElementById("user-link-modal").href = userLink;
    document.getElementById("user-link-modal").innerText = userLinkText;
    document.getElementById("user-picture-modal").src = userPic;
    document.getElementById("quote-like-count-modal").innerText = likeCount;
    document.getElementById("quote-date-posted-modal").innerText = datePosted;
    MicroModal.show("modal-1", {
        disableScroll: true,
    });
}
