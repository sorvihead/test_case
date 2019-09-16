from config import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_moment import Moment


db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()
moment = Moment()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    moment.init_app(app)

    from app.main import bp as main
    app.register_blueprint(main)

    return app


from app import models