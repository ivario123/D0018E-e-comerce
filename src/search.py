from flask import Blueprint, request, render_template, session, redirect, url_for
import require as require
from require import response
from flask_login import current_user
from sql.auth import *
from sql.inventory.getters import *
from json import loads



search_blueprint = Blueprint(
    "search", __name__, template_folder="../templates")

def selected_categories():
    categories = request.args.get("categories", default=[])
    categories = loads(categories)
    return categories

def fetch_items(search_input, filter_input):
    if not search_input:
        return redirect(url_for('index'))
    category_input = []
    category_input.append(search_input)
    search_category = get_all_items_with_category(category_input)
    search_input = '%' + search_input + '%'
    search_name = get_item_by_search_name(search_input)
    if search_name is None:
        search_name = []

    # group items from category search with name search
    search_name.extend(item for item in search_category if item not in search_name)

    # TODO only show categories of items in search result
    # need to check categories before filtering after categories to not lose categories from pure search. 
    category_group = super_categories_and_sub()

    # if filtering for categories
    if filter_input:
        selected_cat = selected_categories()
        search_filter = get_all_items_with_category(selected_cat)
        search_name.extend(search_filter)

        seen = set()
        dupes = []

        for item in search_name:
            if item.serial_number in seen:
                dupes.append(item)
            else:
                seen.add(item.serial_number)

        search_name = dupes
    
    for item in search_name:
        item.add_rating(get_average_review_for(item.serial_number))
    
    return render_template("search.html", user=current_user, items=search_name, category_groups = category_group)


@search_blueprint.route("/search", methods=["GET"])
def search_database():
    return fetch_items(request.args.get('q'), request.args.get('categories'))
