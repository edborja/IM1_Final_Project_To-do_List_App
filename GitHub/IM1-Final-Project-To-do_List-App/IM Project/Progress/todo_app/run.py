from src import create_app
import os

app = create_app()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    app.run(debug=True, ssl_context=(
        os.path.join(BASE_DIR, '127.0.0.1+1.pem'),
        os.path.join(BASE_DIR, '127.0.0.1+1-key.pem')
    ))
