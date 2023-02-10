from flask import Blueprint, request, render_template, session, redirect, url_for
import require as require
from require import response
from flask_login import current_user
from sql.auth import *
from sql.inventory.getters import *

search_blueprint = Blueprint("search",__name__,template_folder="../templates",url_prefix="/search")

def fetch_items(search_input):
    search_input = '%' + search_input + '%'
    items_searched = get_item_by_search_name(search_input)
    if items_searched is None:
        items_searched = []
    return render_template("index.html", user = current_user, items=items_searched)
    

@search_blueprint.route("/<string:filter>", methods =["GET"])
def search_database(filter):
    return fetch_items(filter)

# IF SEARCH IS EMPTY
@search_blueprint.route("/", methods=["GET"])
def empty_search():
    items_searched = get_all_items()
    return render_template("index.html", user = current_user, items=items_searched)
