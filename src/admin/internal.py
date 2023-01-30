
from flask import request
from require import fields
from sql.inventory.management import *
from sql.inventory.getters import *
from sql.auth import *


@fields(request)
def create_product_internal(name, price, description, image, category):
    print("create_product_internal with name: " + name + " and price: " + price)
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
        print(
            f"INSERT INTO CATEGORY_ASSIGN VALUES ({get_item_by_name(name)[0].serial_number}, {cat}) WHERE NOT EXISTS (SELECT * FROM CATEGORY_ASSIGN WHERE SN={get_item_by_name(name)[0].serial_number} AND Category={cat});")
        assign_category_to_item(
            SN=get_item_by_name(name)[0].serial_number,
            Category=cat
        )


@fields(request)
def create_category_internal(name, super_category):
    return create_category(Name=name, Super=super_category)


@fields(request)
def create_super_category_internal(name):
    print("create_super_category_internal with name: " + name)
    return create_super_category(Name=name)


@fields(request)
def make_admin_internal(email):
    return make_admin(email)
