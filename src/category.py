from flask.blueprints import Blueprint
from flask import redirect, render_template, request, session
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
    categories = super_categories_and_sub()
    for group in categories:
        for category in group.categories:
            if category.name in session["selected_categories"]:
                category.selected = True
    return categories


@category.route("/", methods=["GET"])
@login_required
def category_page():
    categories = selected_categories()
    if categories == []:
        return redirect("/")
    items = get_all_items_with_category(categories)
    # Save the selected categories
    session["selected_categories"] = categories
    # Set the title
    session["title"] = "Category search"
    # Render the page
    all_categories = select_categories()
    return render_template("category.html", items=items, category=categories,
                           category_groups=all_categories, selected_categories=categories)
