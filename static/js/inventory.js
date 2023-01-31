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
function get_multi_select(id) {
    var select = document.getElementById(id);
    var result = [];
    var options = select && select.options;
    var opt;
    for (var i = 0, iLen = options.length; i < iLen; i++) {
        opt = options[i];
        if (opt.selected) {
            result.push(opt.value || opt.text);
        }
    }
    return result;
}

function submit_form() {
    let [name, description, price, image] = select_elements(["name", "description", "price", "image"]);
    let category = get_multi_select("category")
    console.log(category)

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
            "category": category
        })
    }).then(response => {
        if (response.status == 200) {
            window.location.href = "/"
        }
        else {
            alert("Item creation failed")
            window.location.href = "/admin/create_product"
        }
    })
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
    fetch("/admin/create_super_category", {
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
            window.location.href = "/admin/create_super_category"
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
            "super_category": super_category
        })
    }).then(response => {
        if (response.status == 200) {
            alert("Category creation successful")
            window.location.href = "/admin"
        }
        else {
            alert("Category creation failed")
            window.location.href = "/admin/create_category"
        }
    });
}
