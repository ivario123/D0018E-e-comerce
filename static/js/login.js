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
function submit() {
    var uname = get_el("email").value;
    var pass = get_el("pass").value;
    console.log("Login attempt: " + uname + " " + pass);

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
    let [uname, pass, user_name, name, surname] = select_elements(["email", "pass", "username", "name", "surname"])
    fetch("/register", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "email": uname,
            "password": pass,
            "username": user_name,
            "name": name,
            "surname": surname,
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