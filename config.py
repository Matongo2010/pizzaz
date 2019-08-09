import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY =  'fourseniorsitis'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://moringaschool:matongome9291@localhost/pizza'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    @staticmethod
    def init_app(app):
        pass
    
    class ProdConfig(object):
      SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://moringaschool:matongome9291@localhost/pizza'
    
    class DevConfig(object):
      DEBUG = True

    config_options = {
    'development':DevConfig,
    'production':ProdConfig
}

