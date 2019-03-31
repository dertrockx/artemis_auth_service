from flask_marshmallow import Marshmallow
from .models import Students

ma = Marshmallow()

class StudentSchema(ma.ModelSchema):
	class Meta:
		model = Students
		fields = ('id', 'lrn', 'username', 'firstname', 'middlename', 'lastname')
