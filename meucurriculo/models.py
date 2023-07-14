from meucurriculo import database, login_manager
from flask_login import UserMixin
from datetime import datetime

"""
------------------Arquivo de models para tabelas---------------------

    Arquivo de arquitetura para tabelas do banco de dados. Aqui estão
definidas todas as colunas que iram compor as três tabelas do banco de
dados curriculo.db.
    As tabelas serão Usuário, com as informações pessoais do profissi-
onal detentor da aplicação; a tabela Habilidades, para cadastrar os 
cursos e competencias do profissional; e Experiencia, com as suas expe-
riências profissionais.
    Esta sendo realizado um relacionamento entre as tabelas através 
do campo ID do usuário tanto para habilidades quanto para experiencia,
através do campo id_profissional.

-----------------------Observações importantes------------------------

    Nescessário rodar o arquivo criadb.py para finalizar a criação do 
banco de dados em casos de ambiente de teste (própria máquina).
_____________________________________________________________________

"""


@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))


class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    firstname = database.Column(database.String, nullable=False)
    lastname = database.Column(database.String, nullable=False)
    profissao = database.Column(database.String, nullable=False)
    nascimento = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    logradouro = database.Column(database.String, nullable=False)
    bairro = database.Column(database.String, nullable=False)
    cidade = database.Column(database.String, nullable=False)
    uf = database.Column(database.String, nullable=False)
    cep = database.Column(database.Integer, nullable=False)
    email = database.Column(database.String, nullable=False)
    fone = database.Column(database.String, nullable=False)
    github = database.Column(database.String, nullable=False)
    linkedin = database.Column(database.String, nullable=False)
    facebook = database.Column(database.String, nullable=False)
    instagran = database.Column(database.String, nullable=False)
    objetivo = database.Column(database.Text, nullable=False)
    competencias = database.Column(database.Text, nullable=False)
    foto_perfil = database.Column(database.String, default='default.png')
    qrcode = database.Column(database.String, default='default.png')
    habilidades = database.relationship('Habilidades', backref='profissional', lazy=True)
    experiencias = database.relationship('Experiencias', backref='profissional', lazy=True)


class Habilidades(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    curso = database.Column(database.String, nullable=False)
    tipo_curso = database.Column(database.String, nullable=False)
    escola = database.Column(database.String, nullable=False)
    dataini = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    datafinal = database.Column(database.DateTime, nullable=True)
    competencia = database.Column(database.Text, nullable=False)
    certificado = database.Column(database.String, default='default.png')
    id_profissional = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)


class Experiencias(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    cargo = database.Column(database.String, nullable=False)
    entidade = database.Column(database.String, nullable=False)
    dataadmin = database.Column(database.DateTime, nullable=False)
    datafim = database.Column(database.DateTime, nullable=True)
    atribuicao = database.Column(database.Text, nullable=False)
    conquistas = database.Column(database.Text, nullable=False)
    id_profissional = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
