from flask import jsonify


def register_error_handlers(app):

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': str(error.description) if hasattr(error, 'description') else 'Bad Request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 'Resource not found'
        }), 404

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'success': False,
            'error': 'Server Error'
        }), 500

    @app.errorhandler(Exception)
    def handle_exception(error):
        print(error)
        return jsonify({
            'success': False,
            'error': str(error) or 'Server Error'
        }), 500
