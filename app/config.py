SECRET_KEY = 'secret'
SQLALCHEMY_DATABASE_URI = 'mysql://root:ch2ng34sc5m6ng@localhost/Arachnid'
SQLALCHEMY_TRACK_MODIFICATIONS = False
JWT_SECRET_KEY = 'jwt-secret-key'
SQLALCHEMY_BINDS = {
	'artemis_db' : 'mysql://root:ch2ng34sc5m6ng@localhost/Artemis'
}