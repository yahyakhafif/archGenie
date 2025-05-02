import os
from app import app

PORT = int(os.environ.get('PORT', 8000))

if __name__ == '__main__':
    print(f'Server running on port {PORT}')
    app.run(host='0.0.0.0', port=PORT, debug=True)
