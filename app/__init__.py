from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:lplw0417@localhost:3306/movie'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SECRET_KEY'] = 'ca8fdda5841c4835b3443e8970c34c9f'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['UP_DIR'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/upload/")
db = SQLAlchemy(app)

from .admin import admin_blueprint
from .home import home_blueprint

app.register_blueprint(admin_blueprint, url_prefix='/admin')
app.register_blueprint(home_blueprint)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')
