from flask_restful import Api, Resource, reqparse, request
from flask_jwt_extended import jwt_required

from flask import Blueprint
import requests, json


comment_blueprint = Blueprint('comment', __name__)

api = Api(comment_blueprint)

BASE_ENDPOINT = 'http://127.0.0.1:8002'


class ListCommentAPIView(Resource):
	@jwt_required
	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument('user_id', type=int)
		parser.add_argument('post_id', type=int)
		args = request.args
		data = parser.parse_args() or args
		print(data)
		headers = {
			'Content-Type' : 'application/json'
		}
		response = requests.get(BASE_ENDPOINT + '/comments/', data=json.dumps(data), headers=headers)
		if response.status_code == requests.codes.ok:
			return response.json(), 200
		return {
			"message" : "Error in retrieving comments",
			"details" : response.json()
		}, 400

class DetailCommentAPIView(Resource):
	@jwt_required
	def get(self, comment_id):
		headers = {
			'Content-Type' : "application/json"
		}
		data = {
			'id' : comment_id
		}
		response = requests.get(
				BASE_ENDPOINT + '/comments/detail/',
				data = json.dumps(data),
				headers = headers
			)
		if response.status_code == requests.codes.ok:
			return response.json(), 200
		return {
			"message" : "Error in retrieving comment",
			"details" : response.json()
		},500

	@jwt_required
	def put(self, comment_id):
		parser = reqparse.RequestParser()
		parser.add_argument('content', help='This field is required', required=True)
		data = parser.parse_args()
		data['id'] = comment_id

		headers = {
			'Content-Type' : "application/json"
		}

		response = requests.put(
				BASE_ENDPOINT + '/comments/detail/',
				data = json.dumps(data),
				headers = headers
			)
		if response.status_code == requests.codes.ok:
			return response.json(), 200
		return {
			"message" : "Error in updating comment",
			"details" : response.json()
		}, 400

	@jwt_required
	def delete(self, comment_id):
		data = {
			'id' : comment_id
		}
		headers = {
			'Content-Type' : 'application/json'
		}
		response = requests.delete(
				BASE_ENDPOINT + '/comments/detail/',
				data = json.dumps(data),
				headers = headers
			)
		if response.status_code == requests.codes.ok:
			return response.json(), 200
		return {
			"message" : "Error in deleting comment",
			"details" : response.json()
		}, 400

class CreateCommentAPIView(Resource):
	@jwt_required
	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('content', required=True, help='This field is required')
		parser.add_argument('post_id', required=True, help='This field is required')
		parser.add_argument('user_id', required=True, help='This field is required')


		data = parser.parse_args()

		headers = {
			"Content-Type" : "application/json"
		}

		response = requests.post(
				BASE_ENDPOINT + '/comments/create/',
				data = json.dumps(data),
				headers = headers
			)
		if response.status_code == requests.codes.ok:
			return response.json(), 200
		return {
			"message" : "Error in creating comment",
			"details" : response.json()
		}, 400

api.add_resource(ListCommentAPIView, '/comments/')
api.add_resource(DetailCommentAPIView, "/comments/<int:comment_id>/")
api.add_resource(CreateCommentAPIView, '/comments/create/')