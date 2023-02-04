# Somente variáveis declaradas com letras maiúsculas são 
# importadas por meio do comando app.config.from_pyfile().

import os

SECRET_KEY = 'alura'

SGBD = 'mysql+mysqlconnector'
usuario = 'root'
senha = 'admin'
servidor = 'localhost'
database = 'jogoteca'
porta = '3306'

# A barra invertida depois do igual permite que
# a atribuiçao comece na linha seguinte.
SQLALCHEMY_DATABASE_URI = \
    f'{SGBD}://{usuario}:{senha}@{servidor}:{porta}/{database}'

UPLOAD_PATH = \
    os.path.dirname(os.path.abspath(__file__)) + '/uploads'
