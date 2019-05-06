SECRET_KEY = 'secret'
SQLALCHEMY_DATABASE_URI = 'mysql://root:ch2ng34sc5m6ng@localhost/Arachnid'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_BINDS = {
	'artemis_db' : 'mysql://root:ch2ng34sc5m6ng@localhost/Artemis'
}
JWT_ACCESS_TOKEN_EXPIRES = 60 # 1-minute token
JWT_SECRET_KEY = 'jwt-secret-key'