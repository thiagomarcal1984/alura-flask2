from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

# Se as views não forem importadas, as rotas não são baixadas.
from views import *

if __name__ == '__main__':
    app.run(debug=True)
