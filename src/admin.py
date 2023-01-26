from flask import render_template, request, session
from flask.blueprints import Blueprint
from require import response, fields, admin as admin_required
from sql.inventory import create_item
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
@admin_required()
def create_product():
    print(request.data)
    if request.method == "POST":
        print(request.data)
        return response(create_product_internal(), code=200)
    else:
        session["title"] = "Create product"
        return render_template("admin/create_product.html")
