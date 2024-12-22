from flask_sqlalchemy import SQLAlchemy
import datetime
db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.String(500), primary_key=True, nullable=False)
    fname = db.Column(db.String(16), nullable=False)
    lname = db.Column(db.String(16), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    # Consider hashing for security
    password = db.Column(db.String(1000), nullable=False)
    points = db.Column(db.Integer(), default=0)
    is_admin = db.Column(db.Boolean(), default=False)
    # Relationships


class FollowedCampaign(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.String(500), db.ForeignKey(
        'user.id'), nullable=False)
    campaigns = db.Column(db.String(100), nullable=True, default=None)


class FollowedCharity(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.String(500), db.ForeignKey(
        'user.id'), nullable=False)
    charity_id = db.Column(db.Integer(), db.ForeignKey(
        'charity.id'), nullable=False)


class Charity(db.Model):
    id = db.Column(db.Integer(), unique=True, primary_key=True,autoincrement=True, nullable=False)
    name = db.Column(db.String(100), unique=True, nullable=False)
    address = db.Column(db.String(500), nullable=False)
    # Use Text for longer descriptions
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=True)
    campaigns = db.relationship('Campaign', backref='charity', lazy=True)
    image = db.Column(db.String(255), nullable=True)


class Campaign(db.Model):
    id = db.Column(db.Integer(), unique=True, primary_key=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    # Use Text for longer descriptions
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime(), nullable=False,
    default=datetime.datetime.utcnow)
    reward = db.Column(db.Integer(), default=0, nullable=False)
    # Specify which charity is responsible for this campaign
    charity_id = db.Column(db.Integer(), db.ForeignKey(
        'charity.id', ondelete="CASCADE",onupdate="CASCADE"),nullable=False)
    capacity = db.Column(db.Integer(), default=0)
    image = db.Column(db.String(255), nullable=True)
    author = db.Column(db.String(100),nullable=False , default="Khair")

    # image = db.Column(db.image.png, nullable=False)  # Uncomment when implementing image


class Merch(db.Model):
    id = db.Column(db.Integer(), unique=True, primary_key=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    # Use Text for longer descriptions
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    image = db.Column(db.String(255), nullable=True)
    # image = db.Column(db.image.png, nullable=False)  # Uncomment when implementing image


class RedeemedMerch(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.String(500), db.ForeignKey(
        'user.id'), nullable=False)
    merch_id = db.Column(db.Integer(), db.ForeignKey(
        'merch.id'), nullable=False)
    date = db.Column(db.Date(), nullable=False)  # Date of redemption


class RegisteredCampaign(db.Model):
    user_id = db.Column(db.String(500), db.ForeignKey(
        'user.id'), nullable=False)
    campaign_id = db.Column(db.Integer(), db.ForeignKey(
        'campaign.id'), primary_key=True)
    
class Media(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Auto-incrementing ID
    image_link = db.Column(db.String(500), nullable=False)   
