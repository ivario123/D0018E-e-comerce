from flask import Blueprint, request, render_template, session, redirect, url_for
from flask_paginate import Pagination, get_page_parameter
import require as require
from require import response
from flask_login import current_user
from sql.auth import *
from sql.inventory.getters import *
from json import loads
import category


search_blueprint = Blueprint("search", __name__, template_folder="../templates")


def selected_categories():
    categories = request.args.get("categories", default=[])
    categories = loads(categories)
    return categories


def remove_dupes(items):
    seen = set()
    filtered = []

    for item in items:
        if item.serial_number not in seen:
            filtered.append(item)
            seen.add(item.serial_number)

    return filtered


def filter(search_result):
    selected_cat = selected_categories()
    search_filter = get_all_items_with_category(selected_cat)
    search_result.extend(search_filter)

    seen = set()
    dupes = []

    for item in search_result:
        if item.serial_number in seen:
            dupes.append(item)
        else:
            seen.add(item.serial_number)

    return dupes


def sort(search_result, method):
    if method == "price_asc":
        return sorted(search_result, key=lambda x: x.price)
    elif method == "price_dsc":
        return sorted(search_result, key=lambda x: x.price, reverse=True)
    elif method == "name_asc":
        return sorted(search_result, key=lambda x: x.name)
    else:
        return sorted(search_result, key=lambda x: x.name, reverse=True)


def fetch_all(filter_input, method):
    category_group = super_categories_and_sub()
    search_result = get_all_items()

    # if filtering for categories
    if filter_input:
        search_result = filter(search_result)
        categories = selected_categories()
        session["selected_categories"] = categories

    if method:
        search_result = sort(search_result, method)

    for item in search_result:
        item.add_rating(get_average_review_for(item.serial_number))

    # Pagination
    page = request.args.get(get_page_parameter(), type=int, default=1)
    pagination = Pagination(
        page=page,
        items=search_result,
        total=len(search_result),
        record_name="items",
        per_page=20,
        css_framework="bulma",
    )
    first_index = (pagination.page - 1) + (
        (pagination.per_page - 1) * (pagination.page - 1)
    )
    last_index = (
        (pagination.page - 1)
        + ((pagination.per_page - 1) * (pagination.page - 1))
        + pagination.per_page
    )

    # if filtered by category 
    if filter_input:
        return render_template(
            "search.html",
            user=current_user,
            items=search_result,
            category_groups=category_group,
            category=categories,
            selected_categories=categories,
            pagination=pagination,
            first_index=first_index,
            last_index=last_index,
        )

    return render_template(
        "search.html",
        user=current_user,
        items=search_result,
        category_groups=category_group,
        pagination=pagination,
        first_index=first_index,
        last_index=last_index,
    )


def fetch_items(search_input, filter_input, method):
    search_category = get_all_items_with_category([search_input])
    search_input = f"%{search_input}%"
    search_result = get_item_by_search_name(search_input)
    super_result = get_all_items_with_super(search_input)

    # group items from category search with name search
    search_result.extend(item for item in search_category if item not in search_result)
    search_result.extend(item for item in super_result if item not in search_result)

    # remove duplicates, seems like i get duplicates after extend even when im telling it not to include duplictaes?
    search_result = remove_dupes(search_result)

    # If search is empty
    if search_result == []:
        return render_template(
            "search.html", user=current_user, items=search_result, category_groups=[]
        )

    # Get exact categories
    serial_numbers = []
    for item in search_result:
        serial_numbers.append(item.serial_number)
    exact_category = search_get_categories(serial_numbers)

    # if filtering for categories
    if filter_input:
        search_result = filter(search_result)
        categories = selected_categories()
        session["selected_categories"] = categories

    # if sorting
    if method:
        search_result = sort(search_result, method)

    # get reviews
    for item in search_result:
        item.add_rating(get_average_review_for(item.serial_number))

    # Pagination
    page = request.args.get(get_page_parameter(), type=int, default=1)
    pagination = Pagination(
        page=page,
        items=search_result,
        total=len(search_result),
        record_name="items",
        per_page=20,
        css_framework="bulma",
    )
    first_index = (pagination.page - 1) + (
        (pagination.per_page - 1) * (pagination.page - 1)
    )
    last_index = (
        (pagination.page - 1)
        + ((pagination.per_page - 1) * (pagination.page - 1))
        + pagination.per_page
    )

    # if filtered by category 
    if filter_input:
        return render_template(
            "search.html",
            user=current_user,
            items=search_result,
            category_groups=exact_category,
            category=categories,
            selected_categories=categories,
            pagination=pagination,
            first_index=first_index,
            last_index=last_index,
        )

    return render_template(
        "search.html",
        user=current_user,
        items=search_result,
        category_groups=exact_category,
        pagination=pagination,
        first_index=first_index,
        last_index=last_index,
    )


@search_blueprint.route("/search", methods=["GET"])
def search_database():
    search_input = request.args.get("q")
    if search_input == "null":
        return fetch_all(request.args.get("categories"), request.args.get("sort"))
    else:
        return fetch_items(
            request.args.get("q"),
            request.args.get("categories"),
            request.args.get("sort"),
        )
