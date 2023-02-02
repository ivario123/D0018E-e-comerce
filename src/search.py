from flask import Blueprint, request, render_template, session, redirect, url_for
import require as require
from require import response
from flask_login import current_user
from sql.auth import *
from sql.inventory.getters import *

search_blueprint = Blueprint("search",__name__,template_folder="../templates")

@require.fields(request)
def fetch_items(search_input):
    if not search_input:
        return redirect(url_for('index'))   
    search_input = '%' + search_input + '%'
    items_searched = get_item_by_search_name(search_input)
    if items_searched is None:
        items_searched = []
    return render_template("index.html", user = current_user, items=items_searched)
    

@search_blueprint.route("/search", methods =["GET", "POST"])
def search_database():
    if request.method == "POST":
        session["items"] = fetch_items()
        session["search_check"] = True
        return response(200)
    if request.method == "GET":
        # makes sure that the template returned matches searched, if the url was just typed then return all products
        if session["search_check"]:
            session["search_check"] = False
            return session["items"]
        else:
            return redirect(url_for('index'))
