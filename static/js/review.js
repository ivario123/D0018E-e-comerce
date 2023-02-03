number_of_stars = 0;
function submit_review(id) {
    let review_field = document.getElementsByClassName("textarea")[0];
    let review = review_field.value;
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
            review_field.textContent = "";
            window.location.reload()
        }
        else {
            alert("Review creation failed, maybe you already reviewed this product?")
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