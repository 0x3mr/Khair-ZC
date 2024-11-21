
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from models.dbSchema import db
from apis.routes.auth_login import auth_bp  # Import the auth blueprint
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

    google = oauth.register(
        name='google',
        client_id =  "1070205957080-201e5tsnmaohqueu1e4qhm85765uvgn1.apps.googleusercontent.com",
            project_id = "delta-smile-434501-u3",
            auth_uri = "https://accounts.google.com/o/oauth2/auth",
            token_uri = "https://oauth2.googleapis.com/token",
            auth_provider_x509_cert_url  = "https://www.googleapis.com/oauth2/v1/certs",
            client_secret = "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",
            redirect_uris = [
                "http://127.0.0.1:5000/login/google/authorized"
            ]
    )
    # Register the blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')  # Prefix routes with /auth

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