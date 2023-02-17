"""
The main flask app
"""

from auth import auth_blueprint, login_manager
from search import search_blueprint
from admin import admin
from category import category
from product import product_blueprint
from order import order_blueprint
from user import user_blueprint
from flask import Flask, render_template, session
from flask_login import current_user, login_required
from sql.inventory.getters import *

# Create app
app = Flask(__name__)
app.secret_key = "some good secret key"
# ---

# Register folders
app.template_folder = "../templates"
app.static_folder = "../static"
# ---

blueprints = [search_blueprint, auth_blueprint, admin,
              category, product_blueprint, order_blueprint, user_blueprint]
for blueprint in blueprints:
    app.register_blueprint(blueprint)
app.login_manager = login_manager


@app.route("/")
@login_required
def index():
    session["title"] = "D0018E - Wine Shop"
    category_groups = super_categories_and_sub()
    items = get_all_items()
    for item in items:
        item.add_rating(get_average_review_for(item.serial_number))

    if items is None:
        items = []
    return render_template(
        "index.html", user=current_user, items=items, category_groups=category_groups
    )


if __name__ == "__main__":
    app.debug = True
    app.jinja_env.globals.update(session=session)
    app.jinja_env.globals.update(get_cart_for_user=get_cart_for_user)
    app.jinja_env.globals.update(get_orders_for_user=get_orders_for_user)
    app.jinja_env.globals.update(
        get_recommendations_for_user=get_recommendations_for_user)
    app.jinja_env.globals.update(
        top5_products=top5_products)
    app.run(host="0.0.0.0", port=5000)
