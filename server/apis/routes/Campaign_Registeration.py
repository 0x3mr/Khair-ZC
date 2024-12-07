from flask import Blueprint, request, jsonify


registration_bp = Blueprint('registration', __name__)
@registration_bp.route('/register', methods=['POST'])

def register_user_for_campaign():
    from models.dbSchema import db, User, campaign, Registeredcampaign
    
    """
    API endpoint to register a user for an campaign.
    Requires user authentication.
    """
    data = request.json
    campaign_id = data.get('campaign_id')
    current_id = data.get('current_id')
    if not campaign_id:
        return jsonify({'error': 'campaign ID is required'}), 400

    # Check if the campaign exists
    campaign = campaign.query.get(campaign_id)
    if not campaign:
        return jsonify({'error': 'campaign not found'}), 404

    # Check if the user is already registered for the campaign
    existing_registration = Registeredcampaign.query.filter_by(user_id=current_id, campaign_id=campaign_id).first()
    if existing_registration:
        # User is already registered
        return jsonify({'error': 'User is already registered for this campaign'}), 400

    # Check campaign capacity
    registered_count = Registeredcampaign.query.filter_by(campaign_id=campaign_id).count()
    if registered_count >= campaign.capacity:
        # Insufficient capacity
        return jsonify({'error': 'campaign capacity reached'}), 400

    # Register the user for the campaign
    new_registration = Registeredcampaign(user_id=current_id, campaign_id=campaign_id)
    db.session.add(new_registration)
    db.session.commit()
    # Return success msg
    return jsonify({'message': 'User successfully registered for the campaign'}), 201
