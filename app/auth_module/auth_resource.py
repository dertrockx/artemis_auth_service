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
from .models import Students
from .schema import StudentSchema

auth_blueprint = Blueprint('auth', __name__)
api = Api(auth_blueprint)

user_parser = reqparse.RequestParser()
user_parser.add_argument('username')
user_parser.add_argument('lrn')
user_parser.add_argument('password', help='This field cannot be blank', required=True)

class UserLogin(Resource):
	def post(self):
		data 		= user_parser.parse_args()
		lrn 		= data.get('lrn', None)
		username 	= data.get('username', None)
		password 	= data.get('password')
		student 	= Students.query.filter(or_(Students.lrn == lrn, Students.username == username)).first()
		if not student:
			return {'message': "User not found"}

		if student.check_password(password):	
			access_token = create_access_token(identity = student.username)
			refresh_token = create_refresh_token(identity = student.username)
			return {
					'message': 'Logged in!',
					'access_token' : access_token,
					'refresh_token' : refresh_token
			}
		return {"message" : "Passwords do not match!"}

class UserList(Resource):
	@jwt_required
	def get(self):
		stud_ = StudentSchema()
		students = [ stud_.dump(student).data for student in Students.query.all()]
		return students

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
api.add_resource(UserLogoutRefresh, '/logout/refresh/')
api.add_resource(UserLogoutAccess, '/logout/access/')
api.add_resource(TokenRefresh, '/token/refresh/')
api.add_resource(ProtectedApi, '/protected/')
api.add_resource(UserList, '/users/')