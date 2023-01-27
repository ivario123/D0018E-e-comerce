from flask import render_template, request, session
from flask.blueprints import Blueprint
from require import response, fields, admin as admin_required
from sql.inventory import *
from models import Item

admin = Blueprint("admin", "admin",
                  template_folder="../templates", url_prefix="/admin")


@fields(request)
def create_product_internal(name, price, description, image):
    return create_item(
        ProductName=name,
        Price=price,
        ProductDescription=description,
        Image=image,
        Inventory=0,
    )


def callback_non_admin():
    return render_template("admin/403.html")


@admin.route("/create_product", methods=["GET", "POST"])
# @admin_required()
def create_product():
    print(request.data)
    if request.method == "POST":
        print(request.data)
        return response(create_product_internal(), code=200)
    else:
        session["title"] = "Create product"
        return render_template("admin/create_product.html", super_categories=get_all_categories_grouped_by_supercategory())


@fields(request)
def create_category_internal(name, supercategory):
    print("create_category_internal with name: " +
          name + " and supercategory: " + supercategory)
    return create_category(Name=name, Super=supercategory)


@ admin.route("/create_category", methods=["GET", "POST"])
def create_category_endpoint():
    print("create_category_endpoint")
    if request.method == "POST":
        print("create_category_endpoint POST")
        return response(create_category_internal(), code=200)
    else:
        session["title"] = "Create category"
        return render_template("admin/create_category.html", super_categories=get_all_supercategories())


@ fields(request)
def create_supercategory_internal(name):
    return create_supercategory(Name=name)


@ admin.route("/create_supercategory", methods=["GET", "POST"])
def create_supercategory_endpoint():
    if request.method == "POST":
        return create_supercategory_internal()
    else:
        session["title"] = "Create supercategory"
        return render_template("admin/create_category_group.html")
