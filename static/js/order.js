function remove_all_tasks() {
    // From https://stackoverflow.com/questions/8860188/javascript-clear-all-timeouts
    var id = window.setTimeout(function () { }, 0);
    while (id--) {
        window.clearTimeout(id); // will do nothing if no timeout with id is present
    }
}

async function remove(id) {
    remove_all_tasks();
    const batcher = async () => {
        remove(id)
    }
    // We need to wait for resource lock here since the
    if (lock) {
        setTimeout(
            batcher, 50
        )
        return
    }
    acquire();
    target[id].amount = -1;
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
            "Amount": 0
        })
    }).then(response => {
        if (response.status == 200) {
            target[id].amount = -1;
        }
        else {
            document.getElementById("total_price").innerHTML = old_amount;
            document.getElementById("basket_size").innerHTML += 1;
            parent.appendChild(element);
            alert("404 The sever might be down");
        }
        release();
    })
}
// Crude form of globals with mutex
// Mutex is needed since failover is handled asynchronously 
let target = {};
let retry = false;
let lock = false;
// 2 decorators to make source easier to read
function acquire() {
    lock = true;
}
function release() {
    lock = false;
}
/// This scheduling should be deadlock free, I cannot be bothered to prove it though.
async function batch(id, ordered_amount, total_price, old_ordered_amount, old_total_price, counter = 0) {
    // Batch writes a bunch of stock modifications
    if (!target.hasOwnProperty(id)) {
        // Faulty scheduling
        lock = false
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
    if (lock) {
        // Only retry again if we are the only thread in the queue. 
        if (!retry || target.tries == counter - 1) {
            retry = true;
            target.trei = counter;
            setTimeout(
                batcher, 100
            )
        }
        return
    }
    acquire();
    retry = false;
    // Now we post the new number of elements in the basket
    let base = window.location.origin;
    let old_order = order.amount;
    order.amount = -1;
    fetch(base + "/order/basket/update", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "ProductName": id,
            "Amount": old_order,
        })
    }).then(response => {
        console.log("Completing attempt : " + counter + " For order " + id + " : " + old_order);
        if (response.status == 200) {
            release()
        }
        else {
            ordered_amount.innerHTML = old_ordered_amount;
            total_price.innerHTML = old_total_price;
            release();
            alert("404 The sever might be down");
        }
    })

}

function update_element(id, direction) {
    let product_price = Number(document.getElementById(id + "_orderd_price").innerHTML);
    let ordered_amount = document.getElementById(id + "_ordered_amount");
    let total_price = document.getElementById("total_price");
    let old_total_price = total_price.innerHTML;
    let old_ordered_amount = ordered_amount.innerHTML;
    if (direction) {
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
        "tries": 0
    }
    const batcher = async () => {

        batch(id, ordered_amount, total_price, old_ordered_amount, old_total_price)
    }
    if (!Number(ordered_amount.innerHTML)) {
        remove_all_tasks();
        target[id] = -1;
        remove(id);

    }
    setTimeout(
        batcher, 250
    )



}


function add_to_cart(item_name){
    let amount = document.getElementById("Amount").value;
    console.log(amount);
    let base = window.location.origin;
        
    fetch(base+"/order/basket/add",{
        method:"POST",
        headers: {
            "Content-Type": "application/json"
        },
        body:JSON.stringify({
            "ProductName":item_name,
            "Amount":amount
        })
    }).then(response =>{
        if (response.status == 200){
            window.location.href = "/";
        }
        else{
            alert("Maybe you have already put that item in your cart?");
        }
    })

}