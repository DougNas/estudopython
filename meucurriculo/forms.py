from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, EmailField, TextAreaField, IntegerField, SelectField, DateField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, Email

"""
----------------Arquivo de forms para formulários--------------------


-----------------------Observações importantes------------------------


_____________________________________________________________________

"""

class FormLogin(FlaskForm):
    username = StringField('Username ou Nickname', validators=[DataRequired(), Length(8 , 12)])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 8)])
    lembrar_dados = BooleanField('Lembrar dados de acesso')
    botaoSubmitLogin = SubmitField('Logar')


class FormEnviarEmail(FlaskForm):
    nome = StringField('Nome Completo', validators=[DataRequired()])
    email = EmailField('Seu endereço de E-mail', validators=[DataRequired(), Email()])
    titulo = StringField('Titulo do E-mail', validators=[DataRequired()])
    corpo = TextAreaField('Escreva sua mensagem aqui', validators=[DataRequired()])
    botaoSubmitEnviar = SubmitField('Enviar')


class FormUsuario(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired(), Length(4, 12)])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 10)])
    firstname = StringField('Primeiro Nome', validators=[DataRequired()])
    lastname = StringField('Sobrenome', validators=[DataRequired()])
    profissao = StringField('Ultima Profissão', validators=[DataRequired()])
    nascimento = DateField('Data de Nascimento', validators=[DataRequired()])
    logradouro = StringField('Logadouro c/ número (Rua, Av, Travessa, etc)', validators=[DataRequired()])
    bairro = StringField('Bairro', validators=[DataRequired()])
    cidade = StringField('Cidade', validators=[DataRequired()])
    uf = StringField('UF', validators=[DataRequired(), Length(2)])
    cep = IntegerField('CEP:', validators=[DataRequired()])
    email = EmailField('E-mail', validators=[DataRequired(), Email()])
    fone = StringField('Telefone de contato', validators=[DataRequired()])
    github = StringField('Link para GitHub')
    linkedin = StringField('Link para LinkedIn')
    facebook = StringField('Link para Facebook')
    instagran = StringField('Link para Instagran')
    objetivo = TextAreaField('Digite seus objetivos profissionais', validators=[DataRequired()])
    competencias = TextAreaField('Digite um resumo de suas competências', validators=[DataRequired()])
    foto_perfil = FileField('Atualizar foto Perfil', validators=[FileAllowed(['jpg', 'png'])])
    qrcode = FileField('Atualizar QRCode', validators=[FileAllowed(['jpg', 'png'])])
    botaoSubmitEditar = SubmitField('Confirmar edição')


class FormProfissao(FlaskForm):
    cargo = StringField('Cargo Ocupado', validators=[DataRequired()])
    entidade = StringField('Empresa', validators=[DataRequired()])
    dataadmin = DateField('Data de Admissão', validators=[DataRequired()])
    datafim = DateField('Data de Demissão')
    atribuicao = TextAreaField('Atribuições da Função', validators=[DataRequired()])
    conquistas = TextAreaField('Conquistas profissionais')
    botaoSubmitConfirmarProfissao = SubmitField('Confirmar Experiência')
    id = IntegerField('Selecionar', validators=[DataRequired()])


class FormHabilidades(FlaskForm):
    curso = StringField('Curso', validators=[DataRequired()])
    tipo_curso = SelectField('Tipo de Curso', choices=[('academico', 'Acadêmico'), ('especializacao', 'Especialização'), ('linguas', 'Línguas')], validators=[DataRequired()])
    escola = StringField('Escola', validators=[DataRequired()])
    dataini = DateField('Data de Inicio do Curso', validators=[DataRequired()])
    datafinal = DateField('Data de Termino do Curso')
    competencia = TextAreaField('Competencias desenvolvidas no Curso', validators=[DataRequired()])
    certificado = FileField('Enviar Certificado', validators=[FileAllowed(['jpg', 'png'])])
    botaoSubmitConfirmarCurso = SubmitField('Confirmar Curso')
    id = IntegerField('Selecionar', validators=[DataRequired()])