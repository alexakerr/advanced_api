from flask import Blueprint
from controllers.shoppingCartController import add_cart_item, remove_item_from_cart, update_item_quantity, find_shopping_cart, empty_shopping_cart

shopping_cart_blueprint = Blueprint("shopping_cart_bp", __name__)
shopping_cart_blueprint.route("/add-item", methods=["POST"])(add_cart_item)
shopping_cart_blueprint.route("/remove-item", methods=["DELETE"])(remove_item_from_cart)
shopping_cart_blueprint.route("/update-quantity", methods=["PUT"])(update_item_quantity)
shopping_cart_blueprint.route("/", methods=["GET"])(find_shopping_cart)
shopping_cart_blueprint.route("/empty", methods=["DELETE"])(empty_shopping_cart)