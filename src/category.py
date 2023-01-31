from flask.blueprints import Blueprint
from flask import render_template, request, session
from flask_login import login_required
from require import fields
from sql.inventory.getters import get_all_items_with_category, super_categories_and_sub
from json import loads
import ast
category = Blueprint("category", __name__,
                     template_folder="templates", url_prefix="/category")


def selected_categories():
    categories = request.args.get("categories", default=[])
    categories = loads(categories)
    return categories


def select_categories():
<<<<<<< HEAD
    categories = get_all_categories_grouped_by_super_category()
=======
    categories = super_categories_and_sub()
>>>>>>> 51a9dc9 (Filter on category works, needs a bugfix but that can be merged at a later point)
    for group in categories:
        for category in group.categories:
            if category.name in session["selected_categories"]:
                category.selected = True
    return categories


@category.route("/", methods=["GET"])
@login_required
def category_page():
    categories = selected_categories()
<<<<<<< HEAD
    items = []
    if categories:
        items = valid_items(categories, items)
=======
    items = get_all_items_with_category(categories)
>>>>>>> 51a9dc9 (Filter on category works, needs a bugfix but that can be merged at a later point)
    # Save the selected categories
    session["selected_categories"] = categories
    # Set the title
    session["title"] = "Category search"
    # Render the page
    all_categories = select_categories()
<<<<<<< HEAD
    return render_template('category.html', items=items, category=categories,
=======
    return render_template("category.html", items=items, category=categories,
>>>>>>> 51a9dc9 (Filter on category works, needs a bugfix but that can be merged at a later point)
                           category_groups=all_categories, selected_categories=categories)
