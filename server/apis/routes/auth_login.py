import datetime
from flask import Blueprint, request, jsonify, redirect, url_for, session
from requests_oauthlib import OAuth2Session
import oauthlib
import oauth
from flask_bcrypt import Bcrypt
import regex
from functools import wraps
import cryptography
import jwt
from authlib.integrations.flask_client import OAuth
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from requests_oauthlib import OAuth2Session

auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()
login_manager = LoginManager()

def token_required(f):
    from models.dbSchema import db,User
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            data = jwt.decode(token, auth_bp.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(id=data['user_id']).first()
        except Exception as e:
            return jsonify({'message': 'Token is invalid!'}), 403
        return f(current_user, *args, **kwargs)
    return decorated_function

@auth_bp.route('/register', methods=['POST'])
def register():
    from models.dbSchema import db,User
    
    userId = request.json.get('id')
    firstName = request.json.get('fname')
    lastName = request.json.get('lname')
    password = request.json.get('userPass')
    email = request.json.get('email')

    if not firstName or not lastName  or not password or not email or not userId  :
        return jsonify({"error": "Missing data"}), 400
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "Email already registered"}), 400

    # Create a new user instance
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    new_user = User(id = userId,fname = firstName , lname = lastName , password=hashed_password, email=email )

    # Add the user to the session
    db.session.add(new_user)
    db.session.commit()
    pattern = r'^s-[a-zA-Z]+\.[a-zA-Z]+@zewailcity\.edu\.eg$'


# Check if the email matches the pattern
    if regex.match(pattern, email):
        return jsonify({"message": "User Registered as Zewailian"}), 201
    else:
        return jsonify({"message" :"User Registered as a Guest"}) , 201
    
@auth_bp.route('/login', methods=['POST'])
def login():
    client_id = '1070205957080-201e5tsnmaohqueu1e4qhm85765uvgn1.apps.googleusercontent.com'
    client_secret = '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'
    authorization_base_url = 'https://accounts.google.com/o/oauth2/auth'
    token_url = 'https://accounts.google.com/o/oauth2/token'
    redirect_uri = 'http://127.0.0.1:5000/login/google/authorized'
    scope = ['profile', 'email']
   
    from models.dbSchema import db,User
    email = request.json.get('email')
    password = request.json.get('userPass')
    user = User.query.filter_by(email=email).first()

    if user is None:
        return jsonify({"error": "User not found!"}), 404

    # Check if the provided password matches the stored hash
    if bcrypt.check_password_hash(user.password, password):
        # Password is correct
        token = jwt.encode(
        {'user_id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
        'your_secret_key',  # Your secret key for encoding
        algorithm="HS256"   # The algorithm to use
        )
        return jsonify({"message": "Login successful!" , 'token': token}), 200
    
    else:
        # Password is incorrect
        return jsonify({"error": "Invalid credentials!" ,'token': token}), 401
    
@login_manager.user_loader
def custom_user_loader(user_id):
    """
    Custom callback function to load the user.
    :param user_id: The unique user identifier.
    :return: The User object or None if not found.
    """
    from models.dbSchema import User
    # Query the User table using the provided user_id
    user = User.query.get(user_id)
    # Return the user object if found, otherwise return None
    return user if user else None
    
@auth_bp.route('/',methods=['POST'])
def index():
    if 'google_token' in session:
        user_info = oauth.google.get('https://www.googleapis.com/oauth2/v1/userinfo').json()
        user_info_email = user_info["email"]
        return f'Logged in as {user_info_email}<br><a href="/logout">Logout</a>'
    return 'You are not logged in<br><a href="/login">Login</a>'


@auth_bp.route('/logout')
@login_required
def logout():
    session.pop('google_token', None)
    return redirect(url_for('.index'))

    

