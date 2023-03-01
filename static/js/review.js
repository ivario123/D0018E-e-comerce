number_of_stars = 0;
function submit_review(id) {
    let review_field = document.getElementsByClassName("textarea")[0];
    let review = review_field.value;
    // Reviews need to be valid
    if (review === "") {
        alert("A review needs to have text");
        return
    }
    if (number_of_stars === 0) {
        alert("Number of stars need to be larger than 0");
        return
    }
    // Send data to the server
    fetch("/product/review/new", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "SerialNumber": id,
            "Rating": number_of_stars,
            "Review": review
        })
    }).then(response => {
        if (response.status == 200) {
            review_field.value = "";
            window.location.reload()
        }
        else {
            alert("Review creation failed, maybe you already reviewed this product?")
        }
    })
}

function update_review(id, sn) {
    let review = document.getElementById(id).value;
    // Reviews need to be valid
    if (review === "") {
        alert("A review needs to have text");
        return;
    }
    // Send data to the server
    fetch("/product/review/update", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "SerialNumber": sn,
            "Review": review
        })
    }).then(response => {
        if (response.status == 200) {
            alert("Review updated")
            window.location.reload()
        }
        else {
            alert("Failed to update review")
        }
    })
}

function delete_review(sn) {
    fetch("/product/review/delete", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "SerialNumber": sn,
        })
    }).then(response => {
        if (response.status == 200) {
            alert("Review removed")
            window.location.reload()
        }
        else {
            alert("Failed to delete review")
        }
    })
}

function stars(num) {
    number_of_stars = num;
    for (var i = 1; i <= 5; i++) {
        if (i <= num) {
            document.getElementById("star" + i).style.color = "gold";
        } else {
            document.getElementById("star" + i).style.color = "black";
        }
    }
}
