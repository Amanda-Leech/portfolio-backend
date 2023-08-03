from flask import Flask, request
from sqlalchemy import create_engine
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from db import db, init_db
from model.user import User
from lib.admin import create_admin
from os.path import abspath, dirname, join
import route
import controller

def create_all():
    with app.app_context():
        db.create_all()
        create_admin()

def create_app(config_file=None):
    app = Flask(__name__)
    database_host = "127.0.0.1:5432"
    database_name = "profile"
    engine = create_engine(f'postgresql://{database_host}/{database_name}')
    engine.connect()
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{database_host}/{database_name}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    init_db(app, db)
    current_dir = dirname(abspath(__file__))
    if config_file is None:
        config_file = abspath(join(current_dir, '../config/config.yml'))
    else:
        config_file = abspath(config_file)
    cfg = app.config
    app.env = cfg.get('ENVIRONMENT', 'development')

    if app.debug:
        app.live = False
        if app.env == 'test':
            app.testing = True
        elif app.env == 'development':
            app.dev = True
        else:
            raise EnvironmentError('Invalid environment for app state. (Look inside __init__.py for help)')
    else:
        if app.env == 'production':
            app.live = True
        elif app.env == 'development':
            app.live = False
            app.testing = False
        else:
            raise EnvironmentError('Invalid environment for app state. (Look inside __init__.py for help)')
    return app


app = create_app()
bcrypt = Bcrypt(app)
CORS(app)
ma = Marshmallow(app)

app.register_blueprint(route.auth)
app.register_blueprint(route.about)
app.register_blueprint(route.contact)
app.register_blueprint(route.cover)
app.register_blueprint(route.education)
app.register_blueprint(route.project)
app.register_blueprint(route.resume)
app.register_blueprint(route.skill)
app.register_blueprint(route.user)

@app.route('/user', methods=['PUT'])
def user_update_multi():
    return controller.user_update_multi(request)


create_all()

if __name__ == "__main__":
    app.run(debug=True, port='5000')
