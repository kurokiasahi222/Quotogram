const mainContent = document.querySelector('.main-content');
const sidebar = document.querySelector(".toggler");

console.log("This is a test");

sidebar.addEventListener('change', (event) => {
    if (sidebar.checked) {
        mainContent.classList.add('sidebar-closed');
    } else {
        mainContent.classList.remove('sidebar-closed');
    }
});

window.onload = () => {
    if (sidebar.checked) {
        mainContent.classList.add('sidebar-closed');
    } else {
        mainContent.classList.remove('sidebar-closed');
    }
}
