
from flask_login import login_user
from flask import request, session
import require as require
from result import Result, Ok, Error, to_error
from models import User
from sql.auth import *

# Create nice error messages
NoSuchUser = to_error(
    "No such user", "The login request was for a user that does not exist")
WrongPassword = to_error(
    "Wrong password", "The login request was for a user that does not exist")
InvalidLogin = to_error(
    "Invalid login", "The login request was for a user that does not exist")
# ---


@require.fields(request)
def handle_register(username, email, password, name, surname) -> Result:
    u = User(username=username, email=email, name=name,
             surname=surname, password=password)
    return add_new_user(u)


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
        ok=lambda user: valid_login(user),
        error=lambda x: Error(x)
    )
