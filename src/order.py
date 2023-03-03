from flask.blueprints import Blueprint
from flask_login import login_required
from flask import session, request, render_template
from require import fields
from sql.inventory.management import (
    update_basket,
    remove_element_from_basket,
    add_to_basket,
    checkout_basket,
)

order_blueprint = Blueprint("oder_blueprint", __name__, url_prefix="/order")
basket_blueprint = Blueprint("basket_blueprint", __name__, url_prefix="/basket")
order_blueprint.register_blueprint(basket_blueprint)


@basket_blueprint.route("/update", methods=["POST"])
@login_required
@fields(request)
def update_bakset(ProductName, Amount):
    if Amount == 0 and remove_element_from_basket(session["UID"], ProductName):
        return "Removed element successfully", 200
    if update_basket(session["UID"], ProductName, Amount):
        return "Updated successfully", 200
    return "Error when updating", 400


@basket_blueprint.route("/add", methods=["POST"])
@login_required
@fields(request)
def add_bakset(ProductName, Amount):
    if add_to_basket(session["UID"], ProductName, Amount):
        return "Updated successfully", 200
    return "Error when updating", 400


@fields(request)
def handle_checkout(Address, Zip):
    if checkout_basket(Address=Address, Zip=Zip, UID=session["UID"]):
        return "Checkout complete"
    return "Error in checkout", 400


@order_blueprint.route("/checkout", methods=["GET", "POST"])
@login_required
def endpoint_checkout():
    if request.method == "POST":
        # Handle post
        return handle_checkout()
    else:
        session["title"] = "Checkout"
        # Handle get
        return render_template("checkout.html")
