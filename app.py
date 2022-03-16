from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from models.user import UserModel
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'sam'
api = Api(app)

jwt = JWT(app, authenticate, identity) # /auth
# config JWT to expire within half an hour


api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>') # We are not going to make @app.route(decorator) in restful api
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
