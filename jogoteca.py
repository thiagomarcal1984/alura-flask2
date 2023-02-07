from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
csrf = CSRFProtect(app)

# Se as views não forem importadas, as rotas não são baixadas.
from views_game import *
from views_user import *

if __name__ == '__main__':
    app.run(debug=True)
