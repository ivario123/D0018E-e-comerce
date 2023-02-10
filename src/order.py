from flask.blueprints import Blueprint
from flask_login import login_required
from flask import session, request
from require import fields
from sql.inventory.management import update_basket, remove_element_from_basket,add_to_basket

order_blueprint = Blueprint("oder_blueprint", __name__, url_prefix="/order")
basket_blueprint = Blueprint(
    "basket_blueprint", __name__, url_prefix="/basket")
order_blueprint.register_blueprint(basket_blueprint)


@basket_blueprint.route("/update", methods=["POST"])
@login_required
@fields(request)
def update_bakset(ProductName, Amount):
    if Amount == 0 and remove_element_from_basket(session["email"], ProductName):
        return "Remvoed element successfully",200
    if update_basket(session["email"], ProductName, Amount):
        return "Updated successfully", 200
    return "Error when updating", 400


@basket_blueprint.route("/add", methods=["POST"])
@login_required
@fields(request)
def add_bakset(ProductName, Amount):
    if add_to_basket(session["email"], ProductName, Amount):
        return "Updated successfully", 200
    return "Error when updating", 400
