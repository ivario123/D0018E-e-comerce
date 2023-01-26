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

function valid_email(email) {
    // https://stackoverflow.com/questions/46155/how-to-validate-an-email-address-in-javascript
    var re = /\S+@\S+\.\S+/;
    return re.test(email);
}

function validate_email() {
    var email = get_el("email").value;
    let email_icon_right = document.getElementById("email_icon_right");
    if (!valid_email(email)) {
        // disable the icon
        email_icon_right.disable = true;
        email_icon_right.style.display = "none";
        email_icon_right.style.color = "red"
    }
    else {
        email_icon_right.disable = false;
        email_icon_right.style.display = "";
        email_icon_right.style.color = "green"
    }
}

function submit() {
    var email = get_el("email").value;
    if (!valid_email(email)) {
        alert("Invalid email");
        return;
    }
    var pass = get_el("pass").value;
    console.log("Login attempt: " + email + " " + pass);

    fetch("/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "email": email,
            "password": pass
        })
    }).then(response => {
        console.log(response)
        if (response.status == 200) {
            window.location.href = "/"
        }
        else {
            alert("Login failed").then(
                window.location.href = "/login"
            )
        }
    })
}
function register() {
    let [uname, pass, user_name, name, surname] = select_elements(["email", "pass", "username", "name", "surname"])
    if (!valid_email(email)) {
        alert("Invalid email");
        return;
    }
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