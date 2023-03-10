from flask import render_template, request, session
from flask_login import login_required
from flask.blueprints import Blueprint
from require import response, admin as admin_required
from sql.inventory.management import *
from sql.inventory.getters import *
from sql.auth import *
from admin.internal import *


admin = Blueprint("admin", "admin", template_folder="../templates", url_prefix="/admin")


def non_admin_callback():
    return render_template("errors/403.html", reason="You are not an admin")


@admin.route("/test_database/<template>", methods=["GET"])
def test_database(template):
    """
    Loads a test database
    """
    from json import loads
    import os

    # Load the file
    with open(
        os.path.join(os.path.dirname(__file__), f"examples/{template}.json"), "r"
    ) as f:
        data = loads(f.read())
    for super_category in data["supercategories"]:
        create_super_category(super_category)
    for category in data["categories"]:
        create_category(category["name"], category["super"])
    # Create the items
    for item in data["items"]:
        create_item(
            ProductName=item["ProductName"],
            Price=item["Price"],
            ProductDescription=item["ProductDescription"],
            Image=item["Image"],
            Inventory=item["Inventory"],
        )
        for category in item["Categories"]:
            assign_category_to_item(
                SN=get_item_by_name(item["ProductName"])[0].serial_number,
                Category=category,
            )
    return "Test database created"


@admin.route("/make_admin", methods=["GET", "POST"])
@login_required
# @admin_required(non_admin_callback) # This is commented out because we want to be able to make admins in testing
def make_admin_endpoint():
    if request.method == "POST":
        return response(make_admin_internal(), code=200)
    else:
        session["title"] = "Make admin"
        return render_template("admin/make_admin.html")


def callback_non_admin():
    return render_template("admin/403.html")


@admin.route("/create_product", methods=["GET", "POST"])
@login_required
@admin_required(non_admin_callback)
def create_product():
    if request.method == "POST":
        return response(create_product_internal(), code=200)
    else:
        session["title"] = "Create product"
        return render_template(
            "admin/create_product.html", super_categories=super_categories_and_sub()
        )


@admin.route("/create_category", methods=["GET", "POST"])
@login_required
@admin_required(non_admin_callback)
def create_category_endpoint():
    if request.method == "POST":
        print(request.json)
        return create_category_internal()
    else:
        session["title"] = "Create category"
        return render_template(
            "admin/create_category.html", super_categories=get_all_super_categories()
        )


@admin.route("/create_super_category", methods=["GET", "POST"])
@login_required
@admin_required(non_admin_callback)
def create_super_category_endpoint():
    if request.method == "POST":
        ret = create_super_category_internal()
        return response(ret, code=200 if ret else 400)
    else:
        session["title"] = "Create super_category"
        return render_template(
            "admin/create_category_group.html",
            valid_colors=["primary", "link", "info", "success", "warning", "danger"],
        )


@admin.route("/manage_categories", methods=["GET", "POST"])
@login_required
@admin_required(non_admin_callback)
def manage_categories():
    if request.method == "POST":
        ret = create_super_category_internal()
        return response(ret, code=200 if ret else 400)
    else:
        session["title"] = "Manage categories"
        return render_template(
            "admin/manage_categories.html",
            category_groups=super_categories_and_sub(),
            valid_colors=["primary", "link", "info", "success", "warning", "danger"],
        )


@admin.route("/delete/category", methods=["POST"])
@login_required
@admin_required(non_admin_callback)
@fields(request)
def delete_category(ID: int, Type: str):
    return ("Success", 200) if delete_category_by_name(ID, Type) else ("Error", 400)


@admin.route("/update_super_category/color", methods=["POST"])
@login_required
@admin_required(non_admin_callback)
@fields(request)
def update_super_category_color(ID: int, Color: str):
    return (
        ("Success", 200)
        if update_super_category_color_by_name(ID, Color)
        else ("Error", 400)
    )


@admin.route("/category/name_change", methods=["POST"])
@login_required
@admin_required(non_admin_callback)
@fields(request)
def name_change(Type: str, OldName: str, NewName: str):
    return (
        ("Success", 200)
        if category_name_change(Type, NewName, OldName)
        else ("Error", 400)
    )


@admin.route("/manage_user/<email>", methods=["GET"])
@login_required
@admin_required(non_admin_callback)
def manage_user(email):
    session["title"] = "Manage user"
    user = get_full_user_by_email(Email=email)
    return render_template(
        "user/profile.html",
        user=user,
    )


manage_orders_blueprint = Blueprint(
    "manage_orders", __name__, url_prefix="/manage_orders", static_folder="../static"
)
admin.register_blueprint(manage_orders_blueprint)


@manage_orders_blueprint.route("", methods=["GET"])
@login_required
@admin_required(non_admin_callback)
def manage_orders():
    session["title"] = "Manage orders"
    orders = get_all_orders()
    return render_template("/admin/manage_orders.html", orders=orders)


@manage_orders_blueprint.route("/update", methods=["POST"])
@login_required
@admin_required(non_admin_callback)
@fields(request)
def update_orders():
    body = request.json
    status = body["status"]
    parcelId = body["parcelId"]

    if update_order(status, parcelId):
        return ("Success", 200)
    return (("Error"), 400)


@admin.route("/", methods=["GET"])
@login_required
@admin_required(non_admin_callback)
def index():
    session["title"] = "Admin"
    return render_template("admin/index.html")
