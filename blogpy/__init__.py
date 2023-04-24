from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
import os
import sqlalchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = '4df409def166706112a3727099a842cf'
if os.getenv("DATABASE_URL"):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///waysite.db'

database = SQLAlchemy(app)
app.app_context().push()
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = f"Por Favor, Realize o seu Login!"
login_manager.login_message_category = 'alert-info'

from blogpy import models

engine = sqlalchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
inspection = sqlalchemy.inspect(engine)
if not inspection.has_table('usuario', schema="dbo"):
    with app.app_context():
        database.drop_all()
        database.create_all()
        print('Base de Dados Criada')
else:
    print('Base de Dados já Criada')

from blogpy import routes