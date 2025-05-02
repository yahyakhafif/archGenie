from flask import Blueprint, request, jsonify
from config.db import db
from models.Style import Style, FamousExample
from middleware.auth import protect
from services.recommendationService import get_time_based_recommendations, get_replacement_recommendation

styles_bp = Blueprint('styles', __name__)


@styles_bp.route('/', methods=['GET'])
def get_all_styles():
    try:
        styles = Style.query.order_by(Style.name.asc()).all()
        return jsonify([s.to_dict() for s in styles]), 200
    except Exception as e:
        print(str(e))
        return 'Server Error', 500


@styles_bp.route('/recommendations', methods=['GET'])
@protect
def get_recommendations():
    try:
        limit = request.args.get('limit', 3, type=int)
        exclude_ids_str = request.args.get('exclude', '')
        exclude_ids = [int(x) for x in exclude_ids_str.split(',') if x.strip()] if exclude_ids_str else []

        recommendations = get_time_based_recommendations(
            request.user.id,
            limit,
            exclude_ids
        )

        return jsonify([s.to_dict() for s in recommendations]), 200

    except Exception as e:
        print(f'Recommendation error: {str(e)}')
        return jsonify({
            'success': False,
            'message': 'Error getting recommendations'
        }), 500


@styles_bp.route('/recommendations/replacement', methods=['GET'])
@protect
def get_replacement():
    try:
        current_ids_str = request.args.get('current', '')
        current_ids = [int(x) for x in current_ids_str.split(',') if x.strip()] if current_ids_str else []

        replacement = get_replacement_recommendation(
            request.user.id,
            current_ids
        )

        if not replacement:
            return jsonify({
                'success': False,
                'message': 'No more recommendations available'
            }), 404

        return jsonify(replacement.to_dict()), 200

    except Exception as e:
        print(f'Replacement recommendation error: {str(e)}')
        return jsonify({
            'success': False,
            'message': 'Error getting replacement recommendation'
        }), 500


@styles_bp.route('/search/<keyword>', methods=['GET'])
def search_styles(keyword):
    try:
        pattern = f'%{keyword}%'
        styles = Style.query.filter(
            db.or_(
                Style.name.ilike(pattern),
                Style.description.ilike(pattern),
                Style.characteristics.any(keyword)
            )
        ).all()

        all_styles = Style.query.all()
        matching_ids = {s.id for s in styles}

        for style in all_styles:
            if style.id not in matching_ids:
                if style.characteristics:
                    for char in style.characteristics:
                        if keyword.lower() in char.lower():
                            styles.append(style)
                            matching_ids.add(style.id)
                            break

        return jsonify([s.to_dict() for s in styles]), 200

    except Exception as e:
        print(str(e))
        return 'Server Error', 500


@styles_bp.route('/', methods=['POST'])
@protect
def create_style():
    data = request.get_json()
    errors = []

    name = data.get('name', '').strip() if data.get('name') else ''
    period = data.get('period', '').strip() if data.get('period') else ''
    description = data.get('description', '').strip() if data.get('description') else ''
    characteristics = data.get('characteristics', [])

    if not name:
        errors.append({'msg': 'Name is required', 'param': 'name'})
    if not period:
        errors.append({'msg': 'Time period is required', 'param': 'period'})
    if not description:
        errors.append({'msg': 'Description is required', 'param': 'description'})
    if not characteristics or not isinstance(characteristics, list) or len(characteristics) < 1:
        errors.append({'msg': 'At least one characteristic is required', 'param': 'characteristics'})

    if errors:
        return jsonify({'errors': errors}), 400

    try:
        existing = Style.query.filter_by(name=name).first()
        if existing:
            return jsonify({'msg': 'Style with this name already exists'}), 400

        new_style = Style(
            name=name,
            period=period,
            description=description,
            characteristics=characteristics,
            main_features=data.get('mainFeatures', []),
            image_url=data.get('imageUrl'),
            created_by=request.user.id
        )

        db.session.add(new_style)
        db.session.flush()

        famous_examples = data.get('famousExamples', [])
        for example in famous_examples:
            fe = FamousExample(
                style_id=new_style.id,
                name=example.get('name'),
                location=example.get('location'),
                architect=example.get('architect'),
                year=example.get('year'),
                image_url=example.get('imageUrl')
            )
            db.session.add(fe)

        db.session.commit()

        return jsonify(new_style.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        print(str(e))
        return 'Server Error', 500


@styles_bp.route('/<int:style_id>', methods=['GET'])
def get_style_by_id(style_id):
    try:
        style = Style.query.get(style_id)

        if not style:
            return jsonify({'msg': 'Style not found'}), 404

        return jsonify(style.to_dict()), 200

    except Exception as e:
        print(str(e))
        return 'Server Error', 500


@styles_bp.route('/<int:style_id>', methods=['PUT'])
@protect
def update_style(style_id):
    try:
        style = Style.query.get(style_id)

        if not style:
            return jsonify({'msg': 'Style not found'}), 404

        if style.created_by != request.user.id:
            return jsonify({'msg': 'Not authorized to update this style'}), 401

        data = request.get_json()
        if 'name' in data:
            style.name = data['name']
        if 'period' in data:
            style.period = data['period']
        if 'description' in data:
            style.description = data['description']
        if 'characteristics' in data:
            style.characteristics = data['characteristics']
        if 'mainFeatures' in data:
            style.main_features = data['mainFeatures']
        if 'imageUrl' in data:
            style.image_url = data['imageUrl']

        if 'famousExamples' in data:
            FamousExample.query.filter_by(style_id=style.id).delete()
            for example in data['famousExamples']:
                fe = FamousExample(
                    style_id=style.id,
                    name=example.get('name'),
                    location=example.get('location'),
                    architect=example.get('architect'),
                    year=example.get('year'),
                    image_url=example.get('imageUrl')
                )
                db.session.add(fe)

        db.session.commit()

        return jsonify(style.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        print(str(e))
        return 'Server Error', 500


@styles_bp.route('/<int:style_id>', methods=['DELETE'])
@protect
def delete_style(style_id):
    try:
        style = Style.query.get(style_id)

        if not style:
            return jsonify({'msg': 'Style not found'}), 404

        if style.created_by != request.user.id:
            return jsonify({'msg': 'Not authorized to delete this style'}), 401

        db.session.delete(style)
        db.session.commit()

        return jsonify({'msg': 'Style removed'}), 200

    except Exception as e:
        db.session.rollback()
        print(str(e))
        return 'Server Error', 500
