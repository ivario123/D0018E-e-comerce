from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask import Blueprint, request, redirect, url_for, render_template, session
import require as require
from result import Result, Ok, Error, to_error
from sql.auth import *
from require import response, fields
from sql.search import *

search_blueprint = Blueprint("search",__name__,template_folder="../templates")

@require.fields(request)
def handle_search(search_input) -> Result:
    return search_db(search_input)

@require.fields(request)
def fetch_items():
    return
    

@search_blueprint.route("/search", methods =["POST"])
def search_database():
    if request.method == "POST":
        item_exist = handle_search().match
        if item_exist:
            session["title"] = "Bolaget SEARCH"
            fetch_items()
            print("fetched")
        #TODO chance return under to the return of fetching correct products
        return item_exist(
            ok = lambda _: response("Search successful", code = 200),
            error = lambda x: response(f"{x[0]}", code=x[1])
        )
    else:
        return response(500)