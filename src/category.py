from flask.blueprints import Blueprint
from flask import render_template, request, session
from flask_login import login_required
from require import fields
from sql.inventory.getters import get_all_items_with_category, get_all_categories_grouped_by_super_category
from json import loads
import ast
category = Blueprint('category', __name__,
                     template_folder='templates', url_prefix='/category')


def valid_items(selected_categories, items) -> list:
    """
    Returns a list of items that are in all the selected categories
    """
    for category in selected_categories:
        # Get all the items with that category
        ret = get_all_items_with_category(category)
        # If this is the first category, add all the items to the list
        if not items:
            items = ret
            continue
        # If there are no items in the list, there are no items in the list
        if not ret:
            items = []
            break
        # If this is not the first category, remove all the items that are not in the list
        for el in items:
            print(f"Item: {el}")
            if el not in ret:
                items.remove(el)
    return items


def selected_categories():
    categories = request.args.get("categories", default=[])
    categories = loads(categories)
    return categories


def select_categories():
    categories = get_all_categories_grouped_by_super_category()
    for group in categories:
        for category in group.categories:
            if category.name in session["selected_categories"]:
                category.selected = True
    return categories


@category.route("/", methods=["GET"])
@login_required
def category_page():
    categories = selected_categories()
    items = []
    if categories:
        items = valid_items(categories, items)
    # Save the selected categories
    session["selected_categories"] = categories
    # Set the title
    session["title"] = "Category search"
    # Render the page
    all_categories = select_categories()
    return render_template('category.html', items=items, category=categories,
                           category_groups=all_categories, selected_categories=categories)
