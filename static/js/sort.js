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

function fold_away(id) {
    var x = document.getElementById("category_group_" + id);
    var icon = document.getElementById(id + "_icon");
    if (x.style.display === "none") {
        x.style.display = "block";
        icon.innerHTML = "<i class='fa fa-caret-down'></i>";

    } else {
        x.style.display = "none";
        icon.innerHTML = "<i class='fa fa-caret-right'></i>";
    }
}
onload = function () {
    categories.forEach(function (category) {
        if (categories.length > 0)
            document.getElementById("filter").style.display = "inline";
        else
            document.getElementById("filter").style.display = "none";
        let el = document.getElementById(category + "_link").parentElement;
        let container = el.parentElement.parentElement.parentElement;
        let header = container.parentElement.children[0].children[0];
        let icon = header.children[0];
        icon.innerHTML = "<i class='fa fa-caret-down'></i>";
        container.style.display = "block";
        el.children[0].style.display = "inline";
    });
};

function update_category(category) {
    if (!categories.includes(category)) {
        document.getElementById(category + "_icon").style.display = "inline";
        categories.push(category);
    }
    else {
        categories.splice(categories.indexOf(category), 1);
        document.getElementById(category + "_icon").style.display = "none";
    }
    if (categories.length > 0)
        document.getElementById("filter").style.display = "inline";
    else
        document.getElementById("filter").style.display = "none";
}
function filter_categories() {
    var url = document.URL;
    url = url.split("&categories=");
    window.location.href = url[0] + "&categories=" + JSON.stringify(categories);
}