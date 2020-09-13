from flask_restful import Api
from flask import Flask
from resources.users import (UserLogin, UserSignup)
from resources.items import (ItemIdResource, ItemResource)
from db import db
from flask_jwt_extended import (
    JWTManager, jwt_required
)

import os

app = Flask(__name__)

# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)

api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['PROPAGATE_EXCEPTIONS'] = True


@app.before_first_request
def create_tables():
    db.create_all()


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add(
        'Access-Control-Allow-Headers',
        'Content-Type,Authorization')
    response.headers.add(
        'Access-Control-Allow-Methods',
        'GET,PUT,POST,DELETE')
    return response


api.add_resource(ItemIdResource, '/items/<int:id>')
api.add_resource(ItemResource, '/items')

api.add_resource(UserLogin, '/login')
api.add_resource(UserSignup, '/signup')

if __name__ == '__main__':
    db.init_app(app)
    app.run(host='127.0.0.1', port=5000, debug=True)
