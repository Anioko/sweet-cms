from flask_login import current_user, login_required

from libs.download_manager import create_compressed_archive
from mycms.admin.models import Module
from mycms.client.models import CartItem, CartSchema
from mycms.decorators import api_route
from flask_restful import Resource, reqparse

from mycms.extensions import db
from mycms.utils import get_current_cart


@api_route("/cart/get", 'get_cart')
class GetCart(Resource):
    def get(self):
        cart = get_current_cart()
        cart_schema = CartSchema()
        res = cart_schema.dump(cart)
        return {
            'status': 1,
            'cart': res,
        }


@api_route("/cart/add", 'add_to_cart')
class AddToCart(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('product_id', help='This field cannot be blank', required=True)
        self.parser.add_argument('product_support', help='This field cannot be blank', default=True, required=False)

    def post(self):
        data = self.parser.parse_args()
        product = Module.query.get(data['product_id'])
        if not product:
            return {
                'status': 0,
                'title': "Error",
                'message': "Couldn't find product to add"
            }
        user_id = None
        if current_user.is_authenticated:
            user_id = current_user.id
        cart = get_current_cart()
        cart_schema = CartSchema()
        cart.user_id = user_id
        cart_item = CartItem.query.filter_by(product=product).filter_by(cart=cart).first()
        if cart_item:
            res = cart_schema.dump(cart)
            return {
                'status': 1,
                'title': "No Changes in Cart",
                'cart': res,
                'message': "Product '{}' is already in cart".format(product.name),
            }
        cart_item = CartItem(
            cart=cart,
            product=product,
            product_support=True if data['product_support'] else False,
            buyer=current_user if current_user.is_authenticated else None,
        )
        cart.step = 1
        db.session.add(cart)
        db.session.add(cart_item)
        db.session.commit()
        db.session.refresh(cart)
        res = cart_schema.dump(cart)
        return {
            'status': 1,
            'title': "Cart Change",
            'cart': res,
            'message': "Item '{}' is in the cart now".format(product.name),
        }


@api_route("/cart/remove", 'remove_from_cart')
class RemoveFromCart(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('product_id', help='This field cannot be blank', required=True)

    def post(self):
        data = self.parser.parse_args()
        product = Module.query.get(data['product_id'])
        if not product:
            return {
                'status': 0,
                'title': "Error",
                'message': "Couldn't find product to add"
            }
        user_id = None
        if current_user.is_authenticated:
            user_id = current_user.id
        cart = get_current_cart()
        cart_schema = CartSchema()
        cart.user_id = user_id
        cart_item = CartItem.query.filter_by(product=product).filter_by(cart=cart).all()
        if cart_item:
            for item in cart_item: db.session.delete(item)
        db.session.commit()
        db.session.refresh(cart)
        res = cart_schema.dump(cart)
        return {
            'status': 1,
            'title': "Cart Change",
            'cart': res,
            'message': "Item '{}' has been removed from cart".format(product.name),
        }


@api_route('/generate_archive', 'generate_archive')
class GenerateArchive(Resource):

    @login_required
    def post(self):
        try:
            done = create_compressed_archive(current_user.username)
            return {
                'status': 1
            }
        except:
            return {
                'status': 0
            }
