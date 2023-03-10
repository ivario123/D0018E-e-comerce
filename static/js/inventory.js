
old = "details";
function select(id) {
    if (id === old)
        return;
    target_tag = document.getElementById(id + "_tag");
    target_body = document.getElementById(id + "_body");
    old_tag = document.getElementById(old + "_tag");
    old_body = document.getElementById(old + "_body");
    old = id;

    old_tag.classList.remove("is-active");
    target_tag.classList.add("is-active");

    target_body.style.display = "block";
    old_body.style.display = "none";


}

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
    if (price <= 0) {
        alert("Price needs to be higher than 0");
        return;
    }
    let category = get_multi_select("category")

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

let group_color = "";
function select_color(color) {
    if (group_color) {
        document.getElementById(group_color).style.textDecoration = "";
    }
    document.getElementById(color).style.textDecoration = "underline";
    group_color = color;
}

function submit_super_category() {
    let name = get_el("name").value;
    fetch("/admin/create_super_category", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "name": name,
            "color": group_color
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
            "Name": name,
            "SID": Number(super_category)
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

function stock_update(SN) {
    let stock = document.getElementById("stock_amount").value;
    if (stock < 0) {
        alert("Stock needs to be >= 0");
        return;
    }
    fetch("/product/change_stock", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "SN": Number(SN),
            "stock": Number(stock)
        })
    }).then(response => {
        if (response.status == 200) {
            window.location.reload()
            alert("Stock updated!")
        }
        else {
            alert("The stock did not update.");
        }
    })
}

function price_update(SN) {
    let price = document.getElementById("price_amount").value;
    if (price <= 0) {
        alert("Price needs to be higher than 0");
        return;
    }

    fetch("/product/change_price", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "SN": Number(SN),
            "price": Number(price)
        })
    }).then(response => {
        if (response.status == 200) {
            window.location.reload()
            alert("Price updated!")
        }
        else {
            alert("The price did not update.");
        }
    })
}

function close_all_modals() {
    let modals = document.querySelectorAll(".modal");
    for (let i = 0; i < modals.length; i++) {
        modals[i].classList.remove("is-active");
    }
}
function toggle_modal(id) {
    let modal = document.getElementById(id);
    let bkgr = modal.querySelector(".modal-background");
    bkgr.addEventListener("click", function (e) {
        close_all_modals()
    });
    modal.classList.add("is-active");

}