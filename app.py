import os
from flask import Flask, request, abort, jsonify, render_template
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

    @app.route('/')
    def index():
        return render_template('index.html', login_url=os.environ['LOGIN_URL'],
                               github_url=os.environ['GITHUB_URL'])

    @app.route('/login-confirmation')
    def confirm_login():
        return render_template('login-confirm.html')

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
