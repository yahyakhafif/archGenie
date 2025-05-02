from flask import Blueprint, request, jsonify
from config.db import db
from models.User import User
from models.Style import Style
from middleware.auth import protect

users_bp = Blueprint('users', __name__)


@users_bp.route('/favorites', methods=['GET'])
@protect
def get_favorites():
    try:
        user = User.query.get(request.user.id)

        if not user:
            return jsonify({'msg': 'User not found'}), 404

        favorites = [style.to_dict() for style in user.favorites.all()]
        return jsonify(favorites), 200

    except Exception as e:
        print(str(e))
        return 'Server Error', 500


@users_bp.route('/favorites/<int:style_id>', methods=['PUT'])
@protect
def toggle_favorite(style_id):
    try:
        user = User.query.get(request.user.id)

        if not user:
            return jsonify({'msg': 'User not found'}), 404

        style = Style.query.get(style_id)
        if not style:
            return jsonify({'msg': 'Style not found'}), 404

        is_already_favorite = style in user.favorites.all()

        if is_already_favorite:
            user.favorites.remove(style)
            action = 'removed'
        else:
            user.favorites.append(style)
            action = 'added'

        db.session.commit()

        return jsonify({
            'success': True,
            'favorites': [str(s.id) for s in user.favorites.all()],
            'action': action
        }), 200

    except Exception as e:
        db.session.rollback()
        print(str(e))
        return 'Server Error', 500


@users_bp.route('/', methods=['GET'])
@protect
def get_all_users():
    try:
        users = User.query.all()
        return jsonify([u.to_dict() for u in users]), 200
    except Exception as e:
        print(str(e))
        return 'Server Error', 500


@users_bp.route('/<int:user_id>', methods=['GET'])
@protect
def get_user_by_id(user_id):
    try:
        user = User.query.get(user_id)

        if not user:
            return jsonify({'msg': 'User not found'}), 404

        return jsonify(user.to_dict()), 200

    except Exception as e:
        print(str(e))
        return 'Server Error', 500
