from flask import Blueprint, request, jsonify
from models.dbSchema import db, Merch
from apis.routes.Security import session_required, admin_required
from models.Notifications import ErrorProcessor
from datetime import datetime

shop_bp = Blueprint('shop', __name__)

# Error handling abstraction
class ErrorHandler:
    def __init__(self, processor):
        self.processor = processor

    def handle_error(self, error_code, status_code):
        return self.processor.process_error(error_code), status_code


error_handler = ErrorHandler(ErrorProcessor())

# Service for product operations
class ProductService:
    def get_all_products(self):
        return Merch.query.all()

    def add_product(self, name, description, price, image):
        new_product = Merch(name=name, description=description, price=price, image=image)
        db.session.add(new_product)
        db.session.commit()

    def product_exists(self, name):
        return Merch.query.filter_by(name=name).first()


product_service = ProductService()

# Validator for product data
class ProductValidator:
    @staticmethod
    def validate_product_data(data):
        required_fields = ['name', 'description', 'price', 'image']
        if not all(data.get(field) for field in required_fields):
            raise ValueError("shop_missing_fields")

        if not isinstance(data['price'], (int, float)) or data['price'] <= 0:
            raise ValueError("shop_invalid_price")


@shop_bp.route('/products', methods=['GET'])
def get_products():
    products = product_service.get_all_products()
    if not products:
        return error_handler.handle_error("shop_no_products", 404)

    json_products = [
        {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "image": product.image
        }
        for product in products
    ]
    return jsonify(json_products), 200


@shop_bp.route('/products/add', methods=['POST'])
def add_products():
    try:
        product_data = request.json

        # Validate product data
        ProductValidator.validate_product_data(product_data)

        name = product_data['name']
        description = product_data['description']
        price = product_data['price']
        image = product_data['image']

        # Check for duplicate product
        if product_service.product_exists(name):
            return error_handler.handle_error("shop_duplicate_product", 400)

        # Add product to database
        product_service.add_product(name, description, price, image)
        return error_handler.handle_error("shop_product_added", 201)

    except ValueError as e:
        return error_handler.handle_error(str(e), 400)
    except Exception:
        db.session.rollback()
        return error_handler.handle_error("shop_add_product_error", 500)
