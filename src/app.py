"""
The main flask app
"""

from auth import auth_blueprint, login_manager
from admin import admin
from category import category
from flask import Flask, render_template, request, redirect, url_for, flash, session
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

app.register_blueprint(auth_blueprint)
app.register_blueprint(admin)
app.register_blueprint(category)
app.login_manager = login_manager


@app.route("/")
@login_required
def index():
    session["title"] = "D0018E - Wine Shop"
    category_groups = get_all_categories_grouped_by_super_category()
    items = get_all_items()
    if items is None:
        items = []
    return render_template("index.html", user=current_user, items=items, category_groups=category_groups)


if __name__ == "__main__":
    import random
    # Generate a random secret key, resetting session every time
    app.secret_key = ["x" for x in range(0, random.randint(0, 100))]
    app.debug = True
    app.run(host="0.0.0.0", port=5000)
