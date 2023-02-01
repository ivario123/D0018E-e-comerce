"""
This file contains defines the blueprint for the auth routes

these endpoints include login, logout and register
"""


from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from flask import Blueprint, request, redirect, url_for, render_template, session
import require as require
from result import Result, Ok, Error, to_error
from models import User
from sql.auth import *
from require import response, fields

# Create nice error messages
NoSuchUser = to_error(
    "No such user", "The login request was for a user that does not exist"
)
WrongPassword = to_error(
    "Wrong password", "The login request was for a user that does not exist"
)
InvalidLogin = to_error(
    "Invalid login", "The login request was for a user that does not exist"
)
# ---

login_manager = LoginManager()

auth_blueprint = Blueprint("login", __name__, template_folder="../templates")


@login_manager.user_loader
def load_user(email):
    return get_user_by_email(email)


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("login.login"))


@require.fields(request)
def handle_login(email, password):
    def valid_login(user):
        if not login_user(user):
            return Error((InvalidLogin, 400))
        res = get_user_by_email(email)
        if res is None:
            session["logged_in"] = False
            return Error((NoSuchUser, 400))
        session["email"] = res.email
        session["admin"] = res.role == "admin"
        session["logged_in"] = True
        return Ok(res)

    return auth_user(email, password).match(
        ok=lambda user: valid_login(user), error=lambda x: Error(x)
    )


@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        result = handle_login()
        return result.match(
            ok=lambda _: response("Login successful", code=200),
            error=lambda x: response(f"{x[0]}", code=x[1]),
        )
    else:
        session["title"] = "Login"
        return render_template("login.html")


@require.fields(request)
def handle_register(username, email, password, name, surname) -> Result:
    u = User(
        username=username, email=email, name=name, surname=surname, password=password
    )
    return add_new_user(u)


@auth_blueprint.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        return handle_register().match(
            ok=lambda _: response("Registered"),
            error=lambda x: response(f"{x[0]}", code=x[1]),
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
