
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    fname = db.Column(db.String(16), nullable=False)
    lname = db.Column(db.String(16), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(1000), nullable=False)  # Consider hashing for security
    points = db.Column(db.Integer(), default=0)

    # Relationships
    followed_campaigns = db.relationship('FollowedCampaign', backref='user', lazy=True)
    followed_charities = db.relationship('FollowedCharity', backref='user', lazy=True)
    redeemed_merch = db.relationship('RedeemedMerch', backref='user', lazy=True)
    registered_events = db.relationship('RegisteredEvent', backref='user', lazy=True)

class FollowedCampaign(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    campaigns = db.Column(db.String(100), nullable=True, default=None)

class FollowedCharity(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    charities = db.Column(db.String(100), nullable=True, default=None)

class Charity(db.Model):
    id = db.Column(db.Integer(), unique=True, primary_key=True, nullable=False)
    name = db.Column(db.String(100), unique=True, nullable=False)
    address = db.Column(db.String(1000), nullable=False)
    description = db.Column(db.Text, nullable=False)  # Use Text for longer descriptions
    category = db.Column(db.String(50), nullable=True)
    # logo = db.Column(db.image.png, nullable=False)  # Uncomment when implementing logo

    # Relationship
    events = db.relationship('Event', backref='charity', lazy=True)

class Event(db.Model):
    id = db.Column(db.Integer(), unique=True, primary_key=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)  # Use Text for longer descriptions
    date = db.Column(db.DateTime(), nullable=False)
    reward = db.Column(db.Integer(), default=0, nullable=False)
    charity_id = db.Column(db.Integer(), db.ForeignKey('charity.id'), nullable=False)  # Specify which charity is responsible for this event

    # image = db.Column(db.image.png, nullable=False)  # Uncomment when implementing image

class Merch(db.Model):
    id = db.Column(db.Integer(), unique=True, primary_key=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)  # Use Text for longer descriptions
    price = db.Column(db.Integer(), nullable=False)
    # image = db.Column(db.image.png, nullable=False)  # Uncomment when implementing image

class RedeemedMerch(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    merch_id = db.Column(db.Integer(), db.ForeignKey('merch.id'), nullable=False)
    date = db.Column(db.Date(), nullable=False)  # Date of redemption

class RegisteredEvent(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)

























# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()

# class User(db.Model):
#     id = db.Column(db.Integer(), primary_key=True, nullable=False)
#     fname = db.Column(db.String(16), nullable=False)
#     lname = db.Column(db.String(16), nullable=False)
#     email = db.Column(db.String(50), unique=True, nullable=False)
#     password = db.Column(db.String(128), nullable=False)  # Consider hashing for security
#     points = db.Column(db.Integer(), default=0)

#     # Relationships
#     followed_campaigns = db.relationship('FollowedCampaign', backref='user', lazy=True)
#     followed_charities = db.relationship('FollowedCharity', backref='user', lazy=True)
#     redeemed_merch = db.relationship('RedeemedMerch', backref='user', lazy=True)
#     registered_events = db.relationship('RegisteredEvent', backref='user', lazy=True)

# class FollowedCampaign(db.Model):
#     id = db.Column(db.Integer(), primary_key=True)
#     user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
#     campaigns = db.Column(db.String(100), nullable=True, default=None)

# class FollowedCharity(db.Model):
#     id = db.Column(db.Integer(), primary_key=True)
#     user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
#     charities = db.Column(db.String(100), nullable=True, default=None)

# class Charity(db.Model):
#     id = db.Column(db.Integer(), unique=True, primary_key=True, nullable=False)
#     name = db.Column(db.String(100), unique=True, nullable=False)
#     address = db.Column(db.String(1000), nullable=False)
#     description = db.Column(db.Text, nullable=False)  # Use Text for longer descriptions
#     category = db.Column(db.String(50), nullable=True)
#     # logo = db.Column(db.image.png, nullable=False)  # Uncomment when implementing logo

#     # Relationship
#     events = db.relationship('Event', backref='charity', lazy=True)

# class Event(db.Model):
#     id = db.Column(db.Integer(), unique=True, primary_key=True, nullable=False)
#     title = db.Column(db.String(100), nullable=False, db_index=True)
#     description = db.Column(db.Text, nullable=False)  # Use Text for longer descriptions
#     date = db.Column(db.DateTime(), nullable=False)
#     reward = db.Column(db.Integer(), default=0, nullable=False, db_index=True)
#     charity_id = db.Column(db.Integer(), db.ForeignKey('charity.id'), nullable=False)  # Specify which charity is responsible for this event

#     # image = db.Column(db.image.png, nullable=False)  # Uncomment when implementing image

# class Merch(db.Model):
#     id = db.Column(db.Integer(), unique=True, primary_key=True, nullable=False)
#     name = db.Column(db.String(100), nullable=False, db_index=True)
#     description = db.Column(db.Text, nullable=False)  # Use Text for longer descriptions
#     price = db.Column(db.Integer(), nullable=False, db_index=True)
#     # image = db.Column(db.image.png, nullable=False)  # Uncomment when implementing image

# class RedeemedMerch(db.Model):
#     id = db.Column(db.Integer(), primary_key=True)
#     user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
#     merch_id = db.Column(db.Integer(), db.ForeignKey('merch.id'), nullable=False)
#     date = db.Column(db.Date(), nullable=False)  # Date of redemption

# class RegisteredEvent(db.Model):
#     id = db.Column(db.Integer(), primary_key=True)
#     user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
#     event_id = db.Column(db.Integer(), db.ForeignKey('event.id'), nullable=False)