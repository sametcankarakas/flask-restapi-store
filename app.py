import os

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.user import UserRegister, User, UserLogin
from resources.item import Item, ItemList
from models.user import UserModel
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URL','sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPOGATE_EXCEPTIONS'] = True
app.secret_key = 'sam' # app.config['JWT_SECRET_KEY']
api = Api(app)

jwt = JWTManager(app) # not creating /auth
# config JWT to expire within half an hour


api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>') # We are not going to make @app.route(decorator) in restful api
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
