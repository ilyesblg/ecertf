from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt 
from flask_login import LoginManager 
from flask_admin import Admin 
from flask_mail import Mail
from flask_admin.contrib.sqla import ModelView 
app = Flask(__name__) 
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://lysyseasgwadjz:48ed62b33d555c7a848c5bc1eb251e8faea81fbb7a0585e1d0557486c31cb252@ec2-54-208-104-27.compute-1.amazonaws.com:5432/d2tonnr2oba59s'
db = SQLAlchemy(app) 
bcrypt = Bcrypt(app) 
login_manager = LoginManager(app)
login_manager.login_view = 'login' 
login_manager.login_message_category = 'info' 
mail = Mail(app)



from ecert import routes