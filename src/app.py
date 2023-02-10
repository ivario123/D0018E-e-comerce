"""
The main flask app
"""

from auth import auth_blueprint, login_manager
from search import search_blueprint
from admin import admin
from category import category
from product import product_blueprint
from order import order_blueprint
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

app.register_blueprint(search_blueprint)
app.register_blueprint(auth_blueprint)
app.register_blueprint(admin)
app.register_blueprint(category)
app.register_blueprint(product_blueprint)
app.register_blueprint(order_blueprint)
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
    app.run(host="0.0.0.0", port=5000)
