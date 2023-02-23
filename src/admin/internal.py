from flask import request
from require import fields
from sql.inventory.management import *
from sql.inventory.getters import *
from sql.auth import *


@fields(request)
def create_product_internal(name, price, description, image, category):
    create_item(
        ProductName=name,
        Price=price,
        ProductDescription=description,
        Image=image,
        Inventory=0,
    )
    if not isinstance(category, list):
        category = [category]
    for cat in category:
        assign_category_to_item(
            SN=get_item_by_name(name)[0].serial_number, Category=cat
        )


@fields(request)
def create_category_internal(name, super_category):
    return create_category(Name=name, Super=super_category)


@fields(request)
def create_super_category_internal(name, color):
    return create_super_category(Name=name, Color=color)


@fields(request)
def make_admin_internal(email):
    return make_admin(email)
