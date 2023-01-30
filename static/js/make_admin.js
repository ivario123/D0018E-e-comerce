
function make_admin() {

    var form = document.getElementById("email");
    var email = form.value;
    console.log(email);
    fetch("/admin/make_admin", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "email": email
        })
    }).then(response => {
        if (response.status == 200) {
            alert("User is now an admin")
            window.location.href = "/admin"
        }
        else {
            alert("Failed to make user an admin")
            window.location.href = "/admin/make_admin"
        }
    })

}