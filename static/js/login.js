function get_el(id) {
    return document.getElementById(id);
}
function submit() {
    var uname = get_el("email").value;
    var pass = get_el("pass").value;
    console.log("Login attempt: " + uname + " " + pass)
    // Sends https post with content type application/json

    fetch("/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "email": uname,
            "password": pass
        })
    }).then(response => {
        console.log(response)
        if (response.status == 200) {
            window.location.href = "/"
        }
        else {
            alert("Login failed")
            window.location.href = "/login"
        }
    })
}
function register() {
    var uname = get_el("email").value;
    var pass = get_el("pass").value;
    console.log("Login attempt: " + uname + " " + pass)
    // Sends https post with content type application/json

    fetch("/register", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "email": uname,
            "password": pass,
            "username": "Bob",
            "name": "Bob",
            "surname": "Bobsson",
            "Role": "User",
        })
    }).then(response => {
        console.log(response)
        if (response.status == 200) {
            window.location.href = "/"
        }
        else {
            alert("Register failed")
            window.location.href = "/register"
        }
    })
}