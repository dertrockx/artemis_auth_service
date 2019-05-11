from flask_restful import Resource, reqparse, Api
from flask import Blueprint
from flask_jwt_extended import (
							create_access_token, 
							create_refresh_token, 
							jwt_required, 
							jwt_refresh_token_required, 
							get_jwt_identity, 
							get_raw_jwt)
from sqlalchemy import or_
from .models import Students, db
from .schema import StudentSchema

auth_blueprint = Blueprint('auth', __name__)
api = Api(auth_blueprint)

user_parser = reqparse.RequestParser()
user_parser.add_argument('username')
user_parser.add_argument('lrn')
user_parser.add_argument('password', help='This field cannot be blank', required=True)

class UserLogin(Resource):
	def post(self):
		try:
			data 		= user_parser.parse_args()
		except ValueError:
			return {"message" : "Data must be in JSON format"}, 400
		lrn 		= data.get('lrn', None)
		username 	= data.get('username', None)
		password 	= data.get('password')
		student 	= Students.query.filter_by(username=username).first()
		if not student:
			return {'message': "User not found", "status": "ERROR"}

		if student.check_password(password):	
			access_token = create_access_token(identity = student.username)
			refresh_token = create_refresh_token(identity = student.username)
			return {
					'message': 'Logged in!',
					'access_token' : access_token,
					'refresh_token' : refresh_token,
					"status": "OK",
					"username": student.username,
					"id": student.id,
			}
		return {"message" : "Passwords do not match!", "status": "ERROR"}

class UserRegistration(Resource):
	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('username', required=True, help='This field is required')
		parser.add_argument('password', required=True, help='This field is required')
		parser.add_argument('firstName', required=True, help='This field is required')
		parser.add_argument('middleName', required=True, help='This field is required')
		parser.add_argument('lastName', required=True, help='This field is required')
		try:
			data = parser.parse_args()
		except ValueError:
			return {"message" : "Data must be in JSON format"}, 400

		username = data.get('username')

		user = Students.query.filter_by(username=username).first()
		if user:
			return { 
				'message' : "User with username \"{}\" is already taken.".format(username),
				"status": "ERROR"
				}

		user = Students(
				username 	= username, 
				firstname 	= data.get('firstName'),
				middlename = data.get('middleName'),
				lastname = data.get('lastName')
			)
		user.set_password(data.get('password'))
		db.session.add(user)
		db.session.commit()
		return { "message" : "Successfully created user!", "user": StudentSchema().dump(user) }


class UserLogout(Resource):
	def post(self):
		parser 	= reqparse.RequestParser()
		try:
			data = parser.parse_args()
		except ValueError:
			return { "message": "Data must be in JSON format", "status": "ERROR" }
		username 	= data.get('username')
		firstName 	= data.get('firstName')
		middleName 	= data.get('middleName')
		lastName 	= data.get('lastName')


class UserLogoutAccess(Resource):
	def post(self):
		return {'message': 'User logout access'}

class UserLogoutRefresh(Resource):
	def post(self):
		return {'message' : 'User logout refresh'}

class TokenRefresh(Resource):
	@jwt_refresh_token_required
	def post(self):
		current_user = get_jwt_identity()
		print(current_user)
		access_token = create_access_token(identity = current_user)
		return {'message' : "Token refresh", 'access_token' : access_token}

class ProtectedApi(Resource):
	@jwt_required
	def post(self):
		return {'message' : 'Accessed'}

api.add_resource(UserLogin, '/login/')
api.add_resource(UserRegistration, '/register/')
api.add_resource(UserLogoutRefresh, '/logout/refresh/')
api.add_resource(UserLogoutAccess, '/logout/access/')
api.add_resource(TokenRefresh, '/token/refresh/')
api.add_resource(ProtectedApi, '/protected/')
