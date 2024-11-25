
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from models.dbSchema import db
from apis.routes.auth_login import auth_bp  # Import the auth blueprint
from apis.routes.create_charity import charity_bp
from apis.routes.create_event import event_bp
from apis.routes.points_system import points_bp
from apis.routes.Campaign_Registeration import registration_bp
from authlib.integrations.flask_client import OAuth
import oauthlib
import oauth

# Initialize the db object
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key' 

    # Load configuration
    app.config.from_object(Config)

    # Initialize SQLAlchemy with the app
    db.init_app(app)
    oauth = OAuth(app)


    # Register the blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')  # Prefix routes with /auth
    app.register_blueprint(charity_bp, url_prefix='/charity')  # Prefix routes with /auth
    app.register_blueprint(event_bp, url_prefix='/event')  # Prefix routes with /auth
    app.register_blueprint(points_bp, url_prefix='/points')  # Prefix routes with /auth
    app.register_blueprint(registration_bp, url_prefix = '/registration') # Prefix routes with /registration


    

    return app

# Create the app instance
app = create_app()

# Ensure tables are created when the app starts
with app.app_context():
    db.create_all()  # Create all the tables defined in models
    print("Tables created successfully!")

# Run the app
if __name__ == '__main__':
    app.run(debug=True)