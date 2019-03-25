from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from auth_module.models import db
from auth_module.auth_resource import auth_blueprint
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'

app.config.from_pyfile('config.py')
db.init_app(app)

jwt = JWTManager(app)

app.register_blueprint(auth_blueprint)

if __name__=='__main__':
	app.run(debug=True)

