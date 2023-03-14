// Code from article: https://medium.com/@andybarefoot/a-masonry-style-layout-using-css-grid-8c663d355ebb
function resizeAllGridItems() {
    const grid = document.querySelector(".popular-posts");
    grid.style.gridAutoRows = "40px";

    const rowHeight = parseInt(window.getComputedStyle(grid).getPropertyValue('grid-auto-rows'));
    const rowGap = parseInt(window.getComputedStyle(grid).getPropertyValue('grid-row-gap'));

    const allItems = document.querySelectorAll(".quote-wrapper");
    for (let i = 0; i < allItems.length; i++) {
        resizeGridItem(allItems[i], rowHeight, rowGap);
    }
}

function resizeGridItem(item, rowHeight, rowGap) {
    let rowSpan = Math.ceil((item.querySelector('.quote').getBoundingClientRect().height + rowGap) / (rowHeight + rowGap));
    item.style.gridRowEnd = `span ${rowSpan}`;
}

function checkQuoteWidth() {
    const allQuotes = document.querySelectorAll(".quote");
    allQuotes.forEach(quote => {
        const addLabel = quote.querySelector(".quote-footer-buttons-add-label");
        if (quote.getBoundingClientRect().width < 360) {
            quote.querySelector(".more-info-button").innerHTML = '<i class="fa-solid fa-circle-info"></i>';
            if(addLabel)
                addLabel.style.display = "none";
        } else {
            quote.querySelector(".more-info-button").innerHTML = "More Info";
            if(addLabel)
                addLabel.style.display = "inline";
        }
    });
}

window.onload = function() {
    resizeAllGridItems();
    checkQuoteWidth();
}

window.addEventListener("resize", resizeAllGridItems);
window.addEventListener("resize", checkQuoteWidth);
