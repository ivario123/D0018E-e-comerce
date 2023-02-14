from flask.blueprints import Blueprint
from flask_login import login_required
from require import fields
from flask import session, request, render_template

user_blueprint = Blueprint("user", __name__, url_prefix="/user")


@user_blueprint.route("/profile", methods=["GET"])
def index():
    print("stuff")
    return render_template("user/profile.html")


@user_blueprint.route("/orders", methods=["GET"])
def orders():
    return render_template("user/orders.html")
