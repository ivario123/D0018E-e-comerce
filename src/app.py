"""
The main flask app
"""

from auth import auth_blueprint, login_manager
from search import search_blueprint
from admin import admin
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import current_user
from sql.inventory import *

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
app.register_blueprint(search_blueprint)
app.login_manager = login_manager


"""
This is where we will define the "main" routes, such as the index page,
product page, etc.
"""


class CategoryGroup:
    def __init__(self, name, categories):
        self.name = name
        self.categories = categories

#TODO List items
@app.route("/")
def index():
    if session.get("logged_in", False) == False:
        return redirect(url_for("login.login"))
    session["title"] = "Bolaget eller något"
    #items = get_item_by_name(ProductName="Goldstrike")
    category_groups = get_all_categories_grouped_by_supercategory()
    items = get_all_items()
    if items is None:
        items = []
    print(items)
    return render_template("index.html", user=current_user, items=items, category_groups=category_groups)

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=5000)
