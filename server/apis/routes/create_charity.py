import datetime
from flask import Blueprint, request, jsonify
from models.dbSchema import db, Charity
from apis.routes.Security import session_required, admin_required
from models.Notifications import ErrorProcessor

charity_bp = Blueprint('charity', __name__)
Notifications = ErrorProcessor()

@charity_bp.route('/create', methods=['POST'])
@admin_required
def create():
    from models.dbSchema import db, Charity

    charity_data = request.json  # Expecting a single charity or a list of charities in the request body

    if not charity_data:
        return jsonify({"error": "Invalid charity data"}), 400

    # If the data is a single charity, convert it into a list
    if isinstance(charity_data, dict):
        charity_data = [charity_data]
    elif not isinstance(charity_data, list):
        return jsonify({"error": "Invalid charity data"}), 400

    created_charities = []

    for charity in charity_data:
        charity_name = charity.get('name')
        charity_address = charity.get('address')
        charity_desc = charity.get('description')
        category_ch=charity.get('category'),
        image_ch=charity.get('image') 

        # Validate required fields
        if not all([charity_name, charity_address, charity_desc, category_ch,image_ch]):
            return jsonify({"error": "Missing required charity fields"}), 400

        # Check if the charity already exists
        if Charity.query.filter_by(name=charity_name).first():
            return jsonify({"error": "Charity already exists"}), 400

        # Create a new charity
        new_charity = Charity(
            name=charity_name,
            address=charity_address,
            description=charity_desc,
            category=category_ch,
            image=image_ch
        )

        db.session.add(new_charity)
        created_charities.append({"charityId": new_charity.id, "charityName": charity_name})

    db.session.commit()
    return jsonify({"message": "Charities created successfully", "charities": created_charities}), 201
