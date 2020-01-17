from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import getenv
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = ("mysql+pymysql://" + getenv('MYSQL_USER') + ":" + getenv('MYSQL_PWD') + "@" + getenv('MYSQL_IP') + "/" + getenv('MYSQL_DB'))
app.config['SECRET_KEY'] = getenv('MYSQL_SK')
FOLDER = os.path.join('Application', 'Images')
app.config['UPLOAD_FOLDER'] = FOLDER
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from application import routes