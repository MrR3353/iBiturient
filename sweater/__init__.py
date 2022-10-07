from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import pymysql  # need for mysql
pymysql.install_as_MySQLdb()

DB_USERNAME = 'root'
DB_PASSWORD = '******'
DB_SERVERNAME = 'localhost'
DB_NAME = 'db'

app = Flask(__name__)
app.secret_key = 'some secret salt'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://' + DB_USERNAME + ':' + DB_PASSWORD + '@' + DB_SERVERNAME + '/' + DB_NAME
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)



from sweater import models, routes

