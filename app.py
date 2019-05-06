from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS

from auth_module.models import db as auth_db
from auth_module.auth_resource import auth_blueprint

from routers.posts_service_router import post_blueprint
from routers.comments_service_router import comment_blueprint

app = Flask(__name__)

CORS(app) # applying flask-cors to allow CORS

app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config.from_pyfile('config.py')
auth_db.init_app(app)
jwt = JWTManager(app)

app.register_blueprint(auth_blueprint)
app.register_blueprint(post_blueprint)
app.register_blueprint(comment_blueprint)


def create_app():
	app = Flask(__name__)
	app.config.from_pyfile('config.py')
	return app
if __name__=='__main__':
	app.run(debug=True, port=8000, host='0.0.0.0')

