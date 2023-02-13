from flask import Blueprint, request, render_template, session, redirect, url_for
import require as require
from require import response
from flask_login import current_user
from sql.auth import *
from sql.inventory.getters import *

search_blueprint = Blueprint(
    "search", __name__, template_folder="../templates")

def fetch_items(search_input):
    if not search_input:
        return redirect(url_for('index'))
    category_input = []
    category_input.append(search_input)
    search_category = get_all_items_with_category(category_input)
    search_input = '%' + search_input + '%'
    search_name = get_item_by_search_name(search_input)
    if search_name is None:
        search_name = []
    search_name.extend(item for item in search_category if item not in search_name)
    for item in search_name:
        item.add_rating(get_average_review_for(item.serial_number))
    return render_template("index.html", user=current_user, items=search_name)


@search_blueprint.route("/search", methods=["GET"])
def search_database():
    return fetch_items(request.args.get('q'))
