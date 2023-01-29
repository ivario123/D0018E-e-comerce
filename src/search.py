from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask import Blueprint, request, redirect, url_for, render_template, session
import require as require
from flask_login import current_user
from result import Result, Ok, Error, to_error
from sql.auth import *
from sql.inventory import *

search_blueprint = Blueprint("search",__name__,template_folder="../templates")

@require.fields(request)
def fetch_items(search_input):
    search_input = '%' + search_input + '%'
    items_searched = get_item_by_search_name(search_input)
    category_groups = get_all_categories_grouped_by_supercategory()
    if items_searched is None:
        items_searched = []
    return render_template("index.html", user = current_user, items=items_searched, category_groups=category_groups)
    

@search_blueprint.route("/search", methods =["GET", "POST"])
def search_database():
    if request.method == "POST":
        session["title"] = "Bolaget SEARCH"
        session["items"] = fetch_items()
        return session["items"]
    if request.method == "GET":
        return session["items"]