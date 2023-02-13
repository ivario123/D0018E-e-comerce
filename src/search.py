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
    search_input = '%' + search_input + '%'
    items_searched = get_item_by_search_name(search_input)
    if items_searched is None:
        items_searched = []
    for item in items_searched:
        item.add_rating(get_average_review_for(item.serial_number))
    return render_template("index.html", user=current_user, items=items_searched)


@search_blueprint.route("/search", methods=["GET"])
def search_database():
    return fetch_items(request.args.get('q'))
