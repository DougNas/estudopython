from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
import sqlalchemy


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

from meucurriculo import models
engine = sqlalchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
inspector = sqlalchemy.inspect(engine)
if not inspector.has_table("usuario"):
    with app.app_context():
        database.drop_all()
        database.create_all()
        usuario1 = Usuario(
            username='UserNick',
            senha='$2b$12$WJXkqsSvWrihzNHlfAvyouqj.GuYtt0YwoG6.E8fE2BAmMAlaKNqK',
            firstname='Novo',
            lastname='Usuário',
            profissao='Profissão',
            logradouro='Rua Nome da Rua, 001',
            bairro='Nome do Bairro',
            cidade='Nome da Cidade',
            uf='UF',
            cep='12345678',
            email='email@dominio.com',
            fone='(11) 9 9999-9999',
            github='#',
            linkedin='#',
            facebook='#',
            instagran='#',
            objetivo='Digitar um resumo de seus objetivos',
            competencias='Digitar um resumo de suas competencias',
            foto_perfil='default.jpg',
            qrcode='default.jpg'
        )
        database.session.add(usuario1)
        database.session.commit()
        print('Tabelas do banco de dados foram criadas com sucesso')
else:
    print('Tabelas já existentes')


from meucurriculo import routes


