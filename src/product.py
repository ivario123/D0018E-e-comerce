from flask.blueprints import Blueprint
from flask_login import login_required, current_user
from flask import request, session, render_template
from require import fields, response
from sql.inventory.getters import super_categories_and_sub, get_all_items, get_item_by_serial_number, get_reviews_for
from sql.inventory.management import create_review


product_blueprint = Blueprint("product", __name__, url_prefix="/product")


@product_blueprint.route("/info/<int:serial_number>", methods=["POST", "GET"])
@login_required
def product_info(serial_number):
    session["title"] = "Product information"
    category_groups = super_categories_and_sub()
    items = get_all_items()
    item = get_item_by_serial_number(serial_number)[0]
    reviews = get_reviews_for(serial_number)
    return render_template("product_info.html", user=current_user, item=item, items=items, category_groups=category_groups, reviews=reviews)


review_blueprint = Blueprint("review", __name__, url_prefix="/review")
product_blueprint.register_blueprint(review_blueprint)


@review_blueprint.route("/new", methods=["POST"])
@login_required
@fields(request)
def new_review(SerialNumber, Review, Rating):
    ret = create_review(
        SerialNumber,
        Review,
        Rating,
        session["email"]
    )
    if ret:
        return response("Review created")
    return response("Error when creating review", code=400)
