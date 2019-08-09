from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
# from app import routes, models

db = SQLAlchemy()
login = LoginManager()
bootstrap = Bootstrap()


def create_app(config_name):

  app = Flask(__name__)
  db.init_app(app)
  
  app.config.from_object(Config)
  
  migrate = Migrate(app, db)
  

  login.login_view ='login'

