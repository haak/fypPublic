from app import create_app, cli
# from app import db
# from app.models import User

app = create_app()
cli.register(app)
