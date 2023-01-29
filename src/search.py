from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask import Blueprint, request, redirect, url_for, render_template, session
import require as require
from result import Result, Ok, Error, to_error
from sql.auth import *
from require import response, fields
from sql.search import *

search_blueprint = Blueprint("search", __name__, template_folder="../templates")



@require.fields(request)
def search_request(search_input) -> Result:
    return search_db(search_input)

@search_blueprint.route("/search", methods=["GET", "POST"])
def search_handle():
    if request.method == "POST":
        result = search_request()
        if result:
            return response(200)
        else:
            return response(500)
    else:
        return redirect(url_for("index"))