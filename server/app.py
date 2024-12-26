from flask_cors import CORS
from authlib.integrations.flask_client import OAuth
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask import Flask, jsonify, render_template
from werkzeug.exceptions import NotFound
from flask_bcrypt import Bcrypt

from models.dbSchema import db

# Import blueprints from respective modules
from apis.routes.auth_login import auth_bp,oauth_bp
from apis.routes.create_charity import charity_bp
from apis.routes.points_system import points_bp
from apis.routes.Campaign_Registeration import registration_bp
from apis.routes.search import search_bp
from apis.routes.join import join_bp
from apis.routes.CampaignManipulation import campaign_bp
from apis.routes.shop import shop_bp
from apis.routes.media import media_bp
from apis.routes.Security import security_bp



bcrypt = Bcrypt()  # Initialize Bcrypt


def create_app():
    
    app = Flask(__name__, static_folder='static', template_folder='templates')
    CORS(app, resources={r"/*": {"origins": ["http://localhost:3000", "http://127.0.0.1:3000"]}}, supports_credentials=True)
    # Load configuration
    app.config.from_object(Config)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    # Initialize extensions
    db.init_app(app)
    oauth = OAuth(app)

    # blueprints
    app.register_blueprint(auth_bp,         url_prefix='/auth')
    app.register_blueprint(charity_bp,      url_prefix='/charity')
    app.register_blueprint(campaign_bp,     url_prefix='/campaign')
    app.register_blueprint(points_bp, url_prefix='/points')
    app.register_blueprint(registration_bp, url_prefix='/registration')
    app.register_blueprint(search_bp,       url_prefix='/search')
    app.register_blueprint(join_bp,         url_prefix='/join')
    app.register_blueprint(shop_bp,         url_prefix='/shop')
    app.register_blueprint(media_bp,        url_prefix='/media' )
    app.register_blueprint(oauth_bp,        url_prefix='/oauth' )
    app.register_blueprint(security_bp,        url_prefix='/security' )

    


    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({"status": "API Gateway is running"}), 200

    @app.route('/')
    def index():
        return render_template('index.html')

    # Error handler for invalid routes
    @app.errorhandler(NotFound)
    def handle_not_found(error):
        return jsonify({"error": "Endpoint not found"}), 404



    return app


# Create and configure the Flask app instance
app = create_app()

# Ensure database tables are created
with app.app_context():
    db.create_all()
    print("Database tables created successfully!")

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    CORS(app, supports_credentials=True)
