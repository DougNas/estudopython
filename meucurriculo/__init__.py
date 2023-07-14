from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
"""
----------------Arquivo de inicialização da aplicação---------------

    Inicialização das configuações de banco de dados e segurança do
site, criando uma chave secreta que não pode ser acessada por fora.
    Arquivo faz a chamada para o routes.py.

----------------------Observações importantes------------------------

    Em caso de criar novo site, substituir a SECRET_KEY por uma chave
de 16 digitos, de preferencia gerada aleatoriamente atraves dos passoa 
abaixo;
    1 - abrir o console do Python;
    2 - importar o secrets (import secrets);
    3 - executar o comando secrets.token_hex(16);
    4 - copiar o codigo gerado e colar na SECRET_KEY;
    
    Configuração da pasta static como padrão do app.
_____________________________________________________________________

"""

app = Flask(__name__)

app.static_folder = 'static'
app.config['SECRET_KEY'] = 'eaa73db843ffcf47037d4cfca2c8c514'
if os.getenv("DATABASE_URL"):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///curriculo.db'

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Está pagina só é acessivel para usuários logados. Por favor faça login.'
login_manager.login_message_category = 'alert-danger'

from meucurriculo import routes

