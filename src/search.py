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
        print("search_request()")
        result = search_request()
        print("search completed")
        return result.match(  
            ok=lambda _: response("Found something", code=200),
            error=lambda x: response("error", code=418)
        )
    else:
        print("badbing")
        return redirect(url_for("index"))