function get_el(id) {
    return document.getElementById(id);
}
function select_elements(elements) {
    var ret = []
    console.log(elements)
    for (var i = 0; i < elements.length; i++) {
        console.log(elements[i])
        ret.push(document.getElementById(elements[i]).value)
    }
    return ret
}