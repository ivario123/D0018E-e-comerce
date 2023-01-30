"""
This file contains defines the blueprint for the auth routes

these endpoints include login, logout and register
"""


from flask_login import LoginManager, logout_user, login_required
from flask import Blueprint, request, redirect, url_for, render_template, session
import require as require
from sql.auth import *
from require import response
from auth.internal import *

login_manager = LoginManager()

auth_blueprint = Blueprint("login", __name__, template_folder="../templates")


@login_manager.user_loader
def load_user(email):
    return get_user_by_email(email)


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("login.login"))


@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        result = handle_login()
        return result.match(
            ok=lambda _: response("Login successful", code=200),
            error=lambda x: response(f"{x[0]}", code=x[1])
        )
    else:
        session["title"] = "Login"
        return render_template("login.html")


@auth_blueprint.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        return handle_register().match(
            ok=lambda _: response("Registered"),
            error=lambda x: response(f"{x[0]}", code=x[1])
        )
    else:
        session["title"] = "Register"
        return render_template("register.html")


@auth_blueprint.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    session["admin"] = False
    session["title"] = "Logout"
    session["email"] = None
    session["logged_in"] = False
    return redirect(url_for("index"))
