import os
import jwt
from functools import wraps
from flask import request, jsonify
from models.User import User


def protect(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        auth_header = request.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]

        if not token:
            return jsonify({
                'success': False,
                'error': 'Not authorized to access this route'
            }), 401

        try:
            decoded = jwt.decode(
                token,
                os.environ.get('JWT_SECRET', 'secret'),
                algorithms=['HS256']
            )

            user = User.query.get(decoded['id'])
            if not user:
                return jsonify({
                    'success': False,
                    'error': 'Not authorized to access this route'
                }), 401

            request.user = user

        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return jsonify({
                'success': False,
                'error': 'Not authorized to access this route'
            }), 401

        return f(*args, **kwargs)

    return decorated
