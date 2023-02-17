from flask.blueprints import Blueprint
from flask import redirect, render_template, request, session
from flask_login import login_required
from flask_paginate import Pagination, get_page_parameter
from require import fields
from sql.inventory.getters import get_all_items_with_category, super_categories_and_sub
from json import loads
import ast

category = Blueprint(
    "category", __name__, template_folder="templates", url_prefix="/category"
)


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
    # Pagination
    page = request.args.get(get_page_parameter(), type=int, default=1)
    pagination = Pagination(page=page, items=items, total=len(items), record_name='items', per_page=20, css_framework='bulma')
    first_index = (pagination.page-1)+((pagination.per_page-1)*(pagination.page-1))
    last_index  = (pagination.page-1)+((pagination.per_page-1)*(pagination.page-1))+pagination.per_page
    # Save the selected categories
    session["selected_categories"] = categories
    # Set the title
    session["title"] = "Category search"
    # Render the page
    all_categories = select_categories()
    return render_template(
        "category.html",
        items=items,
        category=categories,
        category_groups=all_categories,
        selected_categories=categories,
        pagination=pagination,
        first_index=first_index,
        last_index=last_index
    )
