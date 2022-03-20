import os

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.user import UserRegister, User, UserLogin, UserLogout, TokenRefresh
from resources.item import Item, ItemList
from models.user import UserModel
from resources.store import Store, StoreList
from blacklist import BLACKLIST

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URL','sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPOGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.secret_key = 'sam' # app.config['JWT_SECRET_KEY']
api = Api(app)



jwt = JWTManager(app) # not creating /auth
# config JWT to expire within half an hour
@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1: # instead of hard-coding, we should read from a config file or a database
        return {'is_admin': True}
    return {'is_admin': False}


@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    app.logger.info("hello ")
    app.logger.info(jwt_payload)
    id_iam_looking_for = jwt_payload['jti']
    return id_iam_looking_for in BLACKLIST

# The following callbacks are used for customizing jwt response/error messages.
# The original ones may not be in a very pretty format (opinionated)
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({
        'description': 'The token has expired.',
        'error': 'token_expired'
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):  # we have to keep the argument here, since it's passed in by the caller internally
    return jsonify({
        'description': 'Signature verification failed.',
        'error': 'invalid_token'
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'description': 'Request does not contain an access token.',
        'error': 'authorization_required'
    }), 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback(jwt_header, jwt_payload):
    return jsonify({
        'description': 'The token is not fresh.',
        'error': 'fresh_token_required'
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return jsonify({
        'description': 'The token has been revoked.',
        'error': 'token_revoked'
    }), 401

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>') # We are not going to make @app.route(decorator) in restful api
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/refresh')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
