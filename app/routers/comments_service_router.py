from flask_restful import Api, Resource, reqparse
from flask_jwt_extended import jwt_required

from flask import Blueprint
import requests, json


comment_blueprint = Blueprint('comment', __name__)

api = Api(comment_blueprint)

BASE_ENDPOINT = 'http://127.0.0.1'

class CustomResource(object):
	parser = reqparse.RequestParser()

class ListCommentAPIView(Resource, CustomResource):
	@jwt_required
	def get(self):
		parser = self.parser
		parser.add_argument('user_id', type=int)
		data = parser.parse_args()
		headers = {
			'Content-Type' : 'application/json'
		}
		user_id = data.get('user_id', None)
		sent_data = {}
		if user_id is not None:
			sent_data['user_id'] = user_id

		response = requests.get(BASE_ENDPOINT + ':8001/posts/', data=json.dumps(sent_data), headers=headers)
		if response.status_code == requests.codes.ok:
			return response.json(), 200
		return 500


api.add_resource(ListPostAPIView, '/posts/')