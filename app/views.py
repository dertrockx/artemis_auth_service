from app import app
from flask import Blueprint
from flask_jwt_extended import (
							jwt_required, 
							get_jwt_identity, 
							)
view_blueprint = Blueprint('view', __name__)


@app.route('/posts/')
def posts():
	pass