function get_el(id) {
    return document.getElementById(id);
}
function select_elements(elements) {
    var ret = []
    for (var i = 0; i < elements.length; i++) {
        ret.push(document.getElementById(elements[i]).value)
    }
    return ret
}