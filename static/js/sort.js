document.addEventListener('DOMContentLoaded', function () {
    var dropdown = document.querySelector('.dropdown');
    dropdown.addEventListener('click', function (event) {
        event.stopPropagation();
        dropdown.classList.toggle('is-active');
    });
});       

function sort(method) {
    const params = new URLSearchParams(window.location.search)
    var search_input = params.get('q')


    var category = params.get('categories')
    if (category == null) {
        window.location.href = "/search?q=" + search_input + "&sort=" + method

    }
    else {
        window.location.href = "/search?q=" + search_input + "&categories=" + category + "&sort=" + method
    }
}
