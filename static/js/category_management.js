function hide() {
    let elements = document.getElementsByClassName("color_selector");
    for (let i = 0; i < elements.length; i++) {
        elements[i].style.display = "none"
    }

}

function show(id) {
    let element = document.getElementById(id + "color_selector");
    if (element.style.display == "none") {
        element.style.display = "block";
    }
    else {
        hide()
    }
}

function input_name(event, type, id) {
    if (event.key != "Enter") {
        return
    }
    let NewName = document.getElementById(id + "_input").value;
    fetch("/admin/category/name_change", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "Type": type,
            "OldName": id,
            "NewName": NewName
        })
    }).then(response => {
        if (response.status == 200) {
            alert("Name updated successfully")
            window.location.href = "/admin/manage_categories"
        }
        else {
            alert("Failed to update name")
            window.location.href = "/admin/manage_categories"
        }
    })

}


function submit_category(group) {
    let name = document.getElementById(group + "_name").value;
    fetch("/admin/create_category", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "Name": name,
            "SID": Number(group)
        })
    }).then(response => {
        if (response.status == 200) {
            alert("Category creation successful")
            window.location.href = "/admin/manage_categories"
        }
        else {
            close_all_modals()
        }
    });

}

function toggle_modal(id) {

    let modal = document.getElementById(id);
    let bkgr = modal.querySelector(".modal-background");
    bkgr.addEventListener("click", function (e) {
        close_all_modals()
    });
    modal.classList.add("is-active");
}


function delete_by_id(type, id) {
    url = "/admin/delete/category";
    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "Name": id,
            "Type": type
        })
    }).then(response => {
        if (response.status == 200) {
            alert("Success")
            window.location.href = "/admin/manage_categories"
        }
        else {
            alert("Failed to remove the item from the server")
            window.location.href = "/admin/manage_categories"
        }
    })
}


function select_color(id, color) {
    let element = document.getElementById(id + "tag");
    fetch("/admin/update_super_category/color", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "ID": Number(id),
            "Color": color
        })
    }).then(response => {
        if (response.status == 200) {
            element.classList = "tag is-" + color;
        }
        else {
            alert("Failed to update color, please try again later")
            window.location.href = "/admin/manage_categories"
        }
    })


}