import re
from flask import Blueprint, request, jsonify
from config.db import db
from models.User import User

auth_bp = Blueprint('auth', __name__)


def validate_email(email):
    pattern = r'^\w+([\.\-]?\w+)*@\w+([\.\-]?\w+)*(\.\w{2,3})+$'
    return re.match(pattern, email) is not None


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    errors = []

    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')

    if not name:
        errors.append({'msg': 'Name is required', 'param': 'name'})
    if not email or not validate_email(email):
        errors.append({'msg': 'Please include a valid email', 'param': 'email'})
    if not password or len(password) < 6:
        errors.append({'msg': 'Please enter a password with 6 or more characters', 'param': 'password'})

    if errors:
        return jsonify({'errors': errors}), 400

    try:
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'msg': 'User already exists'}), 400

        user = User(name=name, email=email)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        token = user.get_signed_jwt_token()

        return jsonify({
            'success': True,
            'token': token
        }), 201

    except Exception as e:
        db.session.rollback()
        print(str(e))
        return 'Server error', 500


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    errors = []

    email = data.get('email', '').strip()
    password = data.get('password', '')

    if not email or not validate_email(email):
        errors.append({'msg': 'Please include a valid email', 'param': 'email'})
    if not password:
        errors.append({'msg': 'Password is required', 'param': 'password'})

    if errors:
        return jsonify({'errors': errors}), 400

    try:
        user = User.query.filter_by(email=email).first()

        if not user:
            return jsonify({'msg': 'Invalid credentials'}), 401

        if not user.check_password(password):
            return jsonify({'msg': 'Invalid credentials'}), 401

        token = user.get_signed_jwt_token()

        return jsonify({
            'success': True,
            'token': token,
            'user': {
                'id': str(user.id),
                'name': user.name,
                'email': user.email
            }
        }), 200

    except Exception as e:
        print(str(e))
        return 'Server error', 500


@auth_bp.route('/me', methods=['GET'])
def get_me():
    from middleware.auth import protect

    @protect
    def _get_me():
        try:
            user = User.query.get(request.user.id)
            return jsonify(user.to_dict()), 200
        except Exception as e:
            print(str(e))
            return 'Server Error', 500

    return _get_me()
