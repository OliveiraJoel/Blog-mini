import os

from flask import Flask
from . import db
from . import auth
from . import blog


def create_app(test_config=None):
    #cria a configura o app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY = 'dev', DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'))

    if test_config is None:
        #carrega a instancia config, se existir, quando não for testado
        app.config.from_pyfile('config.py', silent=True)
    else:
        #carrega a configuracao de teste de passar
        app.config.from_mapping(test_config)
    
    #confirma se existe a instancia
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_db(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')
    
    # @app.teardown_appcontext
    # def shutdown_session(exception=None):
    #     db_session.remove()
    
    return app

