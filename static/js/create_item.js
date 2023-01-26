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
function submit_form() {
    let [name, description, price, image] = select_elements(["name", "description", "price", "image"]);
    fetch("/admin/create_product", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "name": name,
            "description": description,
            "price": price,
            "image": image
        })
    }).then(response => {
        console.log(response)
        if (response.status == 200) {
            window.location.href = "/"
        }
        else {
            alert("Item creation failed")
            window.location.href = "/admin/create_product"
        }
    }
    )
}
