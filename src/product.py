from flask.blueprints import Blueprint
from flask_login import login_required, current_user
from flask import request, session, render_template
from require import fields, response
from sql.inventory.getters import (
    super_categories_and_sub,
    get_all_items,
    get_item_by_serial_number,
    get_reviews_for,
)
from sql.inventory.management import (
    create_review,
    update_stock,
    update_price,
    delete_review,
    update_review,
)


product_blueprint = Blueprint("product", __name__, url_prefix="/product",static_folder="../static")


@product_blueprint.route("/info/<int:serial_number>", methods=["POST", "GET"])
@login_required
def product_info(serial_number):
    session["title"] = "Product information"
    category_groups = super_categories_and_sub()
    items = get_all_items()
    item = get_item_by_serial_number(serial_number)[0]
    reviews = get_reviews_for(serial_number)
    return render_template(
        "product_info.html",
        user=current_user,
        item=item,
        items=items,
        category_groups=category_groups,
        reviews=reviews,
    )


@product_blueprint.route("/change_stock", methods=["POST", "GET"])
@login_required
@fields(request)
def change_stock(SN: int, stock: int):
    ret = update_stock(SN, stock)
    if ret:
        return response("Stock updated")
    return response("Error when updating stock", code=400)


@product_blueprint.route("/change_price", methods=["POST", "GET"])
@login_required
@fields(request)
def change_price(SN: int, price: int):
    ret = update_price(SN, price)
    if ret:
        return response("Price updated")
    return response("Error when updating price", code=400)


review_blueprint = Blueprint("review", __name__, url_prefix="/review")
product_blueprint.register_blueprint(review_blueprint)


@review_blueprint.route("/new", methods=["POST"])
@login_required
@fields(request)
def new_review(SerialNumber: int, Review: str, Rating: int):
    ret = create_review(SerialNumber, Review, Rating, session["UID"])
    if ret:
        return response("Review created")
    return response("Error when creating review", code=400)


@review_blueprint.route("/update", methods=["POST"])
@login_required
@fields(request)
def update_review_endpoint(SerialNumber: int, Review: str):
    ret = update_review(SerialNumber, Review, session["UID"])
    if ret:
        return response("Review updated")
    return response("Error when updating review", code=400)


@review_blueprint.route("/delete", methods=["POST"])
@login_required
@fields(request)
def delete_review_endpoint(SerialNumber: int):
    ret = delete_review(SerialNumber, session["UID"])
    if ret:
        return response("Review updated")
    return response("Error when updating review", code=400)
