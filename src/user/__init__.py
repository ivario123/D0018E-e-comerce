from flask.blueprints import Blueprint
from flask_login import login_required
from require import fields
from flask import session, request, render_template
from sql.auth import get_full_user_by_email, update_user_by_email

user_blueprint = Blueprint("user", __name__, url_prefix="/user")


@user_blueprint.route("/profile", methods=["GET"])
def index():
    print("stuff")
    return render_template("user/profile.html")


@user_blueprint.route("/orders", methods=["GET"])
def orders():
    return render_template("user/orders.html")


@user_blueprint.route("/update", methods=["POST"])
@login_required
@fields(request)
def update_profile(UserName: str, Name: str, Surname: str):
    ret = update_user_by_email(session["email"], UserName, Name, Surname)
    print(ret)
    return ("Success", 200) if ret else ("Error", 400)


@user_blueprint.route("/profile", methods=["GET"])
@login_required
def profile():
    print("stuff")
    return render_template("user/profile.html", user=get_full_user_by_email(session["email"]))
