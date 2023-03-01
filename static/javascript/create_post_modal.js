MicroModal.init();

function displayCreatePostModal() {
    // Update our wording so that it is create post and not edit post
    document.querySelector(".create-post-modal-title-text").innerHTML = "Create Post";
    document.querySelector(".create-post-modal-form-submit").innerHTML = "Post Quote";

    let formText = document.getElementById("form-quote");
    let formAuthor = document.getElementById("form-quote-author");
    let formContext = document.getElementById("form-context");
    let formQuoteId = document.getElementById("form-quote-id");

    // Clear the form
    formText.value = "";
    formAuthor.value = "";
    formContext.value = "";
    formQuoteId.value = "";

    MicroModal.show("create-post-modal", {
        disableScroll: true,
    });
}
