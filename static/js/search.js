function get_el(id) {
    return document.getElementById(id);
}
function select_elements(elements) {
    var ret = [];
    for (var i = 0; i < elements.length; i++) {
        ret.push(document.getElementById(elements[i]).value);
    }
    return ret
}

function input(event) {
    if (event.key == "Enter") {
        submit_search();
    }
}

function submit_search() {
    var search = get_el("search").value;
    if (!search.replace(/\s/g, '').length) {
        window.location.href = "/"
    }
    else {
        window.location.href = "/search?q=" + search

    }
}
