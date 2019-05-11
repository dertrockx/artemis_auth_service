from flask_sqlalchemy import SQLAlchemy
import hashlib, random, string

db = SQLAlchemy()

class Students(db.Model):
	__tablename__ = 'Students'
	id 			= db.Column(db.Integer, primary_key=True)
	# lrn 		= db.Column(db.String(15))
	# classcode 	= db.Column(db.String(30), nullable=True)
	firstname 	= db.Column(db.String(128), nullable=True)
	middlename	= db.Column(db.String(128), nullable=True)
	lastname	= db.Column(db.String(128), nullable=True)
	username	= db.Column(db.String(128), nullable=True)
	password 	= db.Column(db.String(128), nullable=True)
	salt 		= db.Column(db.String(128), nullable=True)
	#active		= db.Column(db.Integer)
	#static 		= db.Column(db.Integer)


	def check_password(self, password):
		hasher = hashlib.sha512()
		hasher.update(password.encode('utf-8') + self.salt.encode('utf-8'))
		hashed_password = hasher.hexdigest()
		if hashed_password == self.password:
			return True
		return False

	def generate_salt(self):
		salt = ''.join([ random.choice(string.digits + string.ascii_uppercase + string.ascii_lowercase ) for x in range(128)])
		self.salt = salt
		return salt

	def set_password(self, password):
		hasher = hashlib.sha512()
		self.generate_salt()
		hasher.update(password.encode('utf-8') + self.salt.encode('utf-8'))
		hashed_password = hasher.hexdigest()
		self.password = hashed_password
		