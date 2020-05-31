from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from models import setup_db


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,POST,PATCH,DELETE')
        return response

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
