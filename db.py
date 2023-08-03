from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask import Flask
from sqlalchemy import engine, create_engine

from lib.loaders import load_models

import os

__all__ = ('db', 'init_db')

# our global DB ojbect (imported by models and views)

# support importing a functioning session query


def init_db(app=None, db=None):
    """Initializes the global database object used by the app."""

    if isinstance(app, Flask) and isinstance(db, SQLAlchemy):
        load_models()
        db.init_app(app)
    else:
        raise ValueError('Cannot init DB without db and app objects.')


app = Flask(__name__)
db = SQLAlchemy()
ma = Marshmallow()
basedir = os.path.abspath(os.path.dirname(__file__))
db_host = '127.0.0.1:5432'
db_name = 'certitrack'
engine = create_engine(f'postgresql://{db_host}/{db_name}')
engine.connect()
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_host}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
query = db.session.query
