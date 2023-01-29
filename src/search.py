from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask import Blueprint, request, redirect, url_for, render_template, session
import require as require
from result import Result, Ok, Error, to_error
from sql.auth import *
from sql.search import *

search_blueprint = Blueprint("search",__name__,template_folder="../templates")

@require.fields(request)
def fetch_items(search_input):
    items_searched = get_item_by_SN(SN=search_input)
    if items_searched is None:
        items_searched = []
    print("fetched")
    print(items_searched)
    return render_template("search.html", items_searched=items_searched)
    

@search_blueprint.route("/search", methods =["POST"])
def search_database():
    if request.method == "POST":
        session["title"] = "Bolaget SEARCH"
        print("fetching")
        return fetch_items()
        
