from app import create_app, auth_db

app = create_app()
with app.app_context():
	auth_db.init_app(app)
	auth_db.create_all()