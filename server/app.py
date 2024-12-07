import oauth
import oauthlib
from authlib.integrations.flask_client import OAuth
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask import Flask, jsonify, render_template
from werkzeug.exceptions import NotFound

from models.dbSchema import db

# Import blueprints from respective modules
from apis.routes.auth_login import auth_bp 
from apis.routes.create_charity import charity_bp
from apis.routes.event import event_bp
from apis.routes.points_system import points_bp
from apis.routes.Campaign_Registeration import registration_bp
from apis.routes.search import serach_bp
from apis.routes.join import join_bp
from apis.routes.user import user_bp



# Function to create and configure the Flask app (API gateway)
def create_app():
    
    app = Flask(__name__, static_folder='static', template_folder='templates')

    # Load configuration
    app.config.from_object(Config)
    app.config['SECRET_KEY'] = 'your_secret_key'

    # Initialize extensions
    db.init_app(app)
    oauth = OAuth(app)

    # blueprints
    app.register_blueprint(auth_bp,         url_prefix='/auth')
    app.register_blueprint(charity_bp,      url_prefix='/charity')
    app.register_blueprint(event_bp,        url_prefix='/event')
    app.register_blueprint(points_bp,       url_prefix='/points')
    app.register_blueprint(registration_bp, url_prefix='/registration')
    app.register_blueprint(serach_bp,       url_prefix='/search')
    app.register_blueprint(join_bp,         url_prefix='/join')
    app.register_blueprint(user_bp,         url_prefix='/user')

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
