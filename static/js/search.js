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

function submit_search(){
    var search = get_el("search").value;
    console.log(search);

    fetch("/search", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "search_input": search
        })
    }).then(response => {
        console.log(response)
        if(response.status == 200){
            alert("Search success")
            //TODO make search show products with matching search_input
            window.location.href = "/admin"
        }
        else {
            alert("Search failed")
            window.location.href = "/"
        }
    })
}