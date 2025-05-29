from flask import Flask
from database import db
from controllers.atividade_route import routes
def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///atividades.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        db.create_all() 

    app.register_blueprint(routes, url_prefix="/api") 

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0",port=5003)

   