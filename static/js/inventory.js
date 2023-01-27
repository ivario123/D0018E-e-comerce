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
    let [name, description, price, image] = select_elements(["name", "description", "price", "image", "category"]);
    //category = category.value;
    let body =

        fetch("/admin/create_product", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                "name": name,
                "description": description,
                "price": price,
                "image": image,
                //"category": category
            })
        }).then(response => {
            console.log(response)
            if (response.status == 200) {
                window.location.href = "/admin"
            }
            else {
                alert("Item creation failed")
                window.location.href = "/admin/create_product"
            }
        }
        )
}
function update_preview() {
    let [img_src, name, price, description] = select_elements(["image", "name", "price", "description"])
    let preview_img = document.getElementById("preview_img")
    let preview_title = document.getElementById("preview_title")
    let preview_price = document.getElementById("preview_price")
    preview_img.src = img_src
    preview_title.innerHTML = name
    preview_price.innerHTML = "Price: " + price
}

function submit_super_category() {
    let name = get_el("name").value;
    fetch("/admin/create_supercategory", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "name": name
        })
    }).then(response => {
        if (response.status == 200) {
            window.location.href = "/admin"
        }
        else {
            alert("Super Category creation failed")
            window.location.href = "/admin/create_supercategory"
        }
    });

}
function submit_category() {
    let name = get_el("name").value;
    let super_category = get_el("super_category").value;
    fetch("/admin/create_category", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "name": name,
            "supercategory": super_category
        })
    }).then(response => {
        if (response.status == 200) {
            console.log(response)
            alert("Category creation successful")
            window.location.href = "/admin"
        }
        else {
            alert("Category creation failed")
            window.location.href = "/admin/create_category"
        }
    });
}
