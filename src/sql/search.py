from result import Result, Error, Ok
from . import ssql
from ssql_builder import SSqlBuilder as ssql_builder
from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, session
from sql.inventory import *

search_blueprint = Blueprint("search", __name__, template_folder="../templates")

def search_db(search_input) -> Result:
    with ssql as (conn, curs):
        curs.execute(
            "SELECT * FROM PRODUCT WHERE SN=%s;", (search_input,)
        )
        if curs.fetchone():
            return Ok(search_input)
        else:
            Error("Failed to search, try again later")

#TODO Add searched items into index template
@search_blueprint.route("/admin")
def index():
    if session.get("logged_in", False) == False:
        return redirect(url_for("login.login"))

    session["title"] = "Bolaget search"
    #items = get_item_by_name(ProductName="Goldstrike")
    category_groups = get_all_categories_grouped_by_supercategory()
    items = get_all_items()
    print(items)
    if items is None:
        items = []

    print(items)
    return render_template("index.html",  items=items, category_groups=category_groups)
