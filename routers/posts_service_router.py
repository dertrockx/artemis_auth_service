from flask_restful import Api, Resource, reqparse, request
from flask_jwt_extended import jwt_required

from flask import Blueprint
import requests, json


post_blueprint = Blueprint('routers', __name__)

api = Api(post_blueprint)

BASE_ENDPOINT = 'http://127.0.0.1:8001'


class ListPostAPIView(Resource):
	@jwt_required
	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument('user_id', type=int)
		data = parser.parse_args()
		args = request.args
		headers = {
			'Content-Type' : 'application/json'
		}
		user_id = data.get('user_id') or args.get('user_id') or None
		print(user_id)
		sent_data = {}
		if user_id is not None:
			sent_data['user_id'] = user_id

		response = requests.get(BASE_ENDPOINT + '/posts/', data=json.dumps(sent_data), headers=headers)
		print(response.json())
		if response.status_code == requests.codes.ok:
			return response.json(), 200
		return response.json(), 500

class CreatePostAPIView(Resource):
	# @jwt_required
	def post(self):
		print("YEAH 1")
		parser = reqparse.RequestParser()
		parser.add_argument('content', help='This field is required', required=True)
		parser.add_argument('student_id', help='This field is required', required=True)

		# TODO: Add a method to check if user exists or not

		data = parser.parse_args()
		headers = {
			"Content-Type" : "application/json"
		}
		print("YEAH 2")
		response = requests.post(
				BASE_ENDPOINT + '/posts/create/',
				data = json.dumps(data),
				headers = headers
			)
		print(response.json())
		if response.status_code == requests.codes.ok:
			return response.json(), 200
		return {
			"message" : "Error in creating post.",
			"details" : response.json()
		}

class DetailPostAPIView(Resource):
	@jwt_required
	def get(self, post_id):
		
		headers = {
			'Content-Type' : 'application/json'
		}
		data = {
			"id" : post_id
		}
		response = requests.get(
						BASE_ENDPOINT + '/posts/detail/',
						data=json.dumps(data),
						headers=headers
						)
		if response.status_code == requests.codes.ok:
			return response.json(), 200
		return {
			"message" : "Post not found"
		}, 404

	@jwt_required
	def put(self, post_id):
		parser = self.parser
		parser.add_argument('content', help='This field is required', required=True)

		data = parser.parse_args()

		content = data.get('content')
		headers = {
			'Content-Type' : 'application/json'
		}
		data = {
			'id' : post_id,
			'content' : content
		}
		response = requests.put(
					BASE_ENDPOINT + '/posts/detail/',
					data = json.dumps(data),
					headers = headers
			)
		if response.status_code == requests.codes.ok:
			return response.json(), 200
		return {
			"message" : "Error! bad request."
		},400

	@jwt_required
	def delete(self, post_id):
		headers = {
			'Content-Type' : 'application/json'
		}
		data = {
			'id' : post_id,
		}
		response = requests.delete(
				BASE_ENDPOINT + '/posts/detail/',
				data = json.dumps(data),
				headers = headers
			)
		return response.json()
		'''
		if response.status_code == requests.codes.ok:
			return response.json(), 200
		return {
			"message" : "Error! Server error"
		},500
		'''
api.add_resource(ListPostAPIView, '/posts/')
api.add_resource(DetailPostAPIView, '/posts/<int:post_id>/')
api.add_resource(CreatePostAPIView, '/posts/create/')