// Crude form of globals with mutex
// Mutex is needed since failover is handled asynchronously 
let target = {};
// 2 decorators to make source easier to read
function acquire(id) {
    if (target.hasOwnProperty(id)) {
        target[id].lock = true;
    }
    else {
        target[id] = {
            "amount": 0,
            "tries": -2,
            "lock": true,
        }
    }
}
function release(id) {

    if (target.hasOwnProperty(id)) {
        target[id].lock = false;
    }
    else {
        target[id] = {
            "amount": -1,
            "tries": -2,
            "lock": false,
        }
    }
}

function locked(id) {
    return target.hasOwnProperty(id) ? target[id].lock : false;
}

function remove_all_tasks() {
    // From https://stackoverflow.com/questions/8860188/javascript-clear-all-timeouts
    var id = window.setTimeout(function () { }, 0);
    while (id--) {
        window.clearTimeout(id); // will do nothing if no timeout with id is present
    }
}

async function remove(id) {
    const batcher = async () => {
        remove(id)
    }
    // There could be operations handling this item, so we need to wait
    if (locked(id)) {
        setTimeout(
            batcher, 50
        )
        return
    }
    acquire(id);
    if (target.hasOwnProperty(id)) {
        target[id].amount = -1;
    }
    let element = document.getElementById(id + "_basket");
    let product_price = Number(document.getElementById(id + "_orderd_price").innerHTML);
    let ordered_amount = Number(document.getElementById(id + "_ordered_amount").innerHTML);
    let old_amount = document.getElementById("total_price").innerHTML;

    document.getElementById("total_price").innerHTML -= product_price * ordered_amount;
    document.getElementById("basket_size").innerHTML -= 1;
    let parent = element.parentElement;

    element.parentElement.removeChild(element);
    let base = window.location.origin;

    fetch(base + "/order/basket/update", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "ProductName": id,
            "Amount": Number(0)
        })
    }).then(response => {
        if (response.status == 200) {
            if (target.hasOwnProperty(id)) {
                target[id].amount = -1;
            }
        }
        else {
            document.getElementById("total_price").innerHTML = old_amount;
            document.getElementById("basket_size").innerHTML += 1;
            parent.appendChild(element);
            alert("404 The sever might be down");
        }
        release(id);
    })
}

/// This scheduling should be deadlock free, I cannot be bothered to prove it though.
async function batch(id, ordered_amount, total_price, old_ordered_amount, old_total_price, counter = 0) {
    // Batch writes a bunch of stock modifications
    if (!target.hasOwnProperty(id)) {
        // Faulty scheduling
        return
    }
    // This is bad practice, very easy to attack.
    // We are evaluating user submitted data
    let order = target[id];
    if (order.amount == -1) {
        return
    }
    const batcher = async () => {
        batch(id, ordered_amount, total_price, old_ordered_amount, old_total_price, counter = counter + 1)
    }
    if (locked(id)) {
        // Only retry again if we are the only thread in the queue. 
        console.log("Retry attempt: " + counter + " for " + id + "");
        if (target.tries == counter - 1 || (counter == 0 && target.tries == 0)) {
            target.tries = counter;
            setTimeout(
                batcher, 250
            )
        }
        return
    }
    acquire(id);
    target.tries = 0;
    // Now we post the new number of elements in the basket
    let base = window.location.origin;
    let old_order = order.amount;
    if (!old_order) {
        // We could ger null here, since order might be from invalid html children
        return
    }
    order.amount = -1;
    fetch(base + "/order/basket/update", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "ProductName": id,
            "Amount": Number(old_order),
        })
    }).then(response => {
        if (response.status == 200) {
            release(id)
        }
        else {
            if (target.amount <= 0) {
                release(id);
                return;
            }
            ordered_amount.innerHTML = old_ordered_amount;
            total_price.innerHTML = old_total_price;
            release(id);
            alert("404 The sever might be down");
        }
    })

}


function update_order_amount(id, direction, stock) {
    let ordered_amount = document.getElementById(id + "_order_amount");
    let old_ordered_amount = ordered_amount.innerHTML;
    if (direction) {
        if (Number(ordered_amount.innerHTML) == stock) {
            return;
        }
        // Added one
        ordered_amount.innerHTML = Number(ordered_amount.innerHTML) + 1;
    }
    else if (Number(old_ordered_amount) > 1) {
        // Removed one
        ordered_amount.innerHTML = Number(ordered_amount.innerHTML) - 1;
    }
}
function update_element(id, direction, stock) {
    let product_price = Number(document.getElementById(id + "_orderd_price").innerHTML);
    let ordered_amount = document.getElementById(id + "_ordered_amount");
    let total_price = document.getElementById("total_price");
    let old_total_price = total_price.innerHTML;
    let old_ordered_amount = ordered_amount.innerHTML;
    if (direction) {
        if (Number(ordered_amount.innerHTML) == stock) {
            return;
        }
        // Added one
        total_price.innerHTML = Number(total_price.innerHTML) + product_price;
        ordered_amount.innerHTML = Number(ordered_amount.innerHTML) + 1;
    }
    else if (Number(old_ordered_amount) != 0) {
        // Removed one
        total_price.innerHTML = Number(total_price.innerHTML) - product_price;
        ordered_amount.innerHTML = Number(ordered_amount.innerHTML) - 1;
    }
    target[id] = {
        "amount": Number(ordered_amount.innerHTML),
        "tries": 0,
        "lock": locked(id),
    }
    const batcher = async () => {

        batch(id, ordered_amount, total_price, old_ordered_amount, old_total_price)
    }
    if (!Number(ordered_amount.innerHTML)) {
        remove_idall_tasks();
        target[id] = -1;
        remove(id);

    }
    setTimeout(
        batcher, 100
    )



}


function add_to_cart(item_name) {
    let amount = document.getElementById(item_name + "_order_amount").innerHTML;
    let base = window.location.origin;

    fetch(base + "/order/basket/add", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "ProductName": item_name,
            "Amount": Number(amount)
        })
    }).then(response => {
        if (response.status == 200) {
            window.location.href = "/";
        }
        else {
            alert("Maybe you have already put that item in your cart?");
        }
    })

}
function submit() {
    let address = document.getElementById("address").value;
    let zip = document.getElementById("zip").value;
    fetch("", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "Address": address,
            "Zip": Number(zip),

        })
    }).then(response => {
        if (response.status == 200) {
            window.location.href = "/"
        }
        else {
            alert("Server returned : " + response.status + " error");
        }
    })
}

function manage_order(order_change){
    var input = order_change.split(',')
    var status = input[0]
    var parcelId = input[1]

    fetch("/admin/manage_orders/update", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "status": Number(status),
            "parcelId": Number(parcelId)
        })
    }).then(response => {
        if (response.status == 200) {
            window.location.reload()
        }
        else {
            alert("Something went wrong");
        }
    })

}