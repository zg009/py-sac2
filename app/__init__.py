
from flask import Flask
import utils

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = 'randomly_generated_key'
    if test_config is None:
        app.config.from_pyfile('config.py',silent=True)
    else:
        app.config.from_mapping(test_config)
    
    @app.route('/hello')
    def hello():
        return 'Hello World!'
    
    from . import auth
    app.register_blueprint(auth.bp)
    
    return app