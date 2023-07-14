import secrets
import os
from flask import render_template, redirect, url_for, flash, request, abort
from meucurriculo import app, database, bcrypt
from meucurriculo.forms import FormLogin, FormEnviarEmail, FormUsuario, FormProfissao, FormHabilidades
from meucurriculo.models import Usuario, Experiencias, Habilidades
from flask_login import login_user, logout_user, current_user, login_required
from PIL import Image
from datetime import datetime

"""
--------------------Arquivo de rotas para HTML----------------------

    Define funções utilizadas para chamar as paginas html, de forma a
garantir que mesmo que o link da pagina mude, só será preciso atualizar
o link na função, não afetando o conjunto do site.
    As funções também agregam as instancias dos objetos forms criados
no arquivo forms.py, possibilitando a utilização nos formulários da 
pagina.

----------------------Descrição da páginas web-----------------------

1 - HOME - Onde será exibido o corriculo. Será permitido visualização por
qualquer visitante, mas apenas usuários logados poderão editar.
2 - USUARIO - Permitir atualização de dados do usuário. Apenas usuários
logados poderão ver ou editar essa pagina.
3 - LOGIN - Permitir que um usuário cadastrado possa acessar a aplicação.
Qualquer visitante poderá ver esta página.
4 - ENVIAR - Enviar uma mensagem para o desenvolvedor do site. Qualquer 
visitante poderá ver esta página.
5 - PERFIL - Permitir que um usuário logado possa atualizar suas infor-
mações de esperiência profissional e cursos. Apenas usuários logados 
poderão ver ou editar essa pagina.

-----------------------Observações importantes------------------------

Funções;
SalvarImagem - Carregar uma imagem selecionada pelo usuário

_____________________________________________________________________

"""

#-----------------------------Funções---------------------------------

def SalvarImagem(imagem):
    # adicionar um código aleatório na foto do perfil
    codigo = secrets.token_hex(8)
    nome, extencao = os.path.splitext(imagem.filename)
    nome_imagem = nome + codigo + extencao
    caminho_imagem = os.path.join(app.root_path, 'static\images', nome_imagem)
    # reduzir o tamanho da imagem
    tamanho = (300, 300)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    # salvar imagem no banco de dados
    imagem_reduzida.save(caminho_imagem)
    return nome_imagem


#-----------------------------Routes---------------------------------

# Atalhos para os links de acesso a redes sociais. Links serão cadastrados
#pelo usuário na pagina usuario.html
@app.route("/navbarg")
def linkgit():
    usuario1 = Usuario.query.filter_by(id=1).first()
    if usuario1.github == '#':
        flash(f'Link para GitHub não foi informado ou está indisponível', 'alert-danger')
        return redirect('/')
    return redirect(usuario1.github)


@app.route("/navbarf")
def linkface():
    usuario1 = Usuario.query.filter_by(id=1).first()
    if usuario1.facebook == '#':
        flash(f'Link para Facebook não foi informado ou está indisponível', 'alert-danger')
        return redirect('/')
    return redirect(usuario1.facebook)


@app.route("/navbari")
def linkinsta():
    usuario1 = Usuario.query.filter_by(id=1).first()
    if usuario1.instagran == '#':
        flash(f'Link para Instagran não foi informado ou está indisponível', 'alert-danger')
        return redirect('/')
    return redirect(usuario1.instagran)


@app.route("/navbarl")
def linkdin():
    usuario1 = Usuario.query.filter_by(id=1).first()
    if usuario1.linkedin == '#':
        flash(f'Link para LinkedIn não foi informado ou está indisponível', 'alert-danger')
        return redirect('/')
    return redirect(usuario1.linkedin)


# Pagina inicial onde será exibido o curriculo. As habilidades serão apresentadas
#ordenadas por tipo de curso, começando por Academico, depois especialização,
#depois línguas, e as experiências profissionais. Sempre do mais atual ao mais antigo.
@app.route("/")
def home():
    usuario1 = Usuario.query.filter_by(id=1).first()
    experiencias = Experiencias.query.order_by(Experiencias.dataadmin.desc())
    habilidades = Habilidades.query.order_by(Habilidades.dataini.desc())
    ordem_curso = ['academico', 'especializacao', 'linguas'] # Definir a ordem em que os cursos são mostrados, de acordo com o tipo de curso
    foto_perfil = url_for('static', filename='images/{}'.format(usuario1.foto_perfil))
    return render_template('home.html',
                           foto_perfil=foto_perfil,
                           usuario1=usuario1,
                           experiencias=experiencias,
                           habilidades=habilidades,
                           ordem_curso=ordem_curso)


# Pagina para edição de informações do usuário. Primeiro acesso tem informações default
@app.route("/usuario", methods=['GET', 'POST'])
@login_required
def usuario():
    form_usuario = FormUsuario()
    if request.method == 'POST' and 'botaoSubmitEditar' in request.form:
        with app.app_context():
            senha_cript = bcrypt.generate_password_hash(form_usuario.senha.data)
            current_user.username = form_usuario.username.data
            current_user.senha = senha_cript
            current_user.firstname = form_usuario.firstname.data
            current_user.lastname=form_usuario.lastname.data
            current_user.profissao=form_usuario.profissao.data
            current_user.nascimento=datetime.strptime(str(form_usuario.nascimento.data), '%Y-%m-%d')
            current_user.logradouro=form_usuario.logradouro.data
            current_user.bairro=form_usuario.bairro.data
            current_user.cidade=form_usuario.cidade.data
            current_user.uf=form_usuario.uf.data
            current_user.cep=form_usuario.cep.data
            current_user.email=form_usuario.email.data
            current_user.fone=form_usuario.fone.data
            current_user.github=form_usuario.github.data
            current_user.linkedin=form_usuario.linkedin.data
            current_user.facebook=form_usuario.facebook.data
            current_user.instagran=form_usuario.instagran.data
            current_user.objetivo=form_usuario.objetivo.data
            current_user.competencias=form_usuario.competencias.data
            if form_usuario.foto_perfil.data:
                nome_imagem = SalvarImagem(form_usuario.foto_perfil.data)
                current_user.foto_perfil = nome_imagem
            if form_usuario.qrcode.data:
                qr_imagem = SalvarImagem(form_usuario.qrcode.data)
                current_user.qrcode = qr_imagem
            database.session.commit()
        flash('Dados atualizados com sucesso!', 'alert-success')
        return redirect(url_for('perfil'))
    elif request.method == "GET":
        form_usuario.username.data = current_user.username
        form_usuario.senha.data = current_user.senha
        form_usuario.firstname.data = current_user.firstname
        form_usuario.lastname.data = current_user.lastname
        form_usuario.profissao.data = current_user.profissao
        form_usuario.nascimento.data = current_user.nascimento
        form_usuario.fone.data = current_user.fone
        form_usuario.email.data = current_user.email
        form_usuario.logradouro.data = current_user.logradouro
        form_usuario.bairro.data = current_user.bairro
        form_usuario.cidade.data = current_user.cidade
        form_usuario.uf.data = current_user.uf
        form_usuario.cep.data = current_user.cep
        form_usuario.facebook.data = current_user.facebook
        form_usuario.instagran.data = current_user.instagran
        form_usuario.linkedin.data = current_user.linkedin
        form_usuario.github.data = current_user.github
        form_usuario.objetivo.data = current_user.objetivo
        form_usuario.competencias.data = current_user.competencias
    return render_template('usuario.html', form_usuario=form_usuario)


# Pagina de login de usuário
@app.route("/login", methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    if 'botaoSubmitLogin' in request.form:
        usuario = Usuario.query.filter_by(username=form_login.username.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            flash(f'Bem vindo(a) {usuario.firstname} {usuario.lastname}, sua seção foi iniciada!', 'alert-success')
            pag_next = request.args.get('next')
            if pag_next:
                return redirect(pag_next)
            else:
                return redirect('/')
            return redirect(url_for('/'))
        else:
            flash('Falha no Login! Tente novamente ou entre em contato com o desenvolvedor.', 'alert-danger')
    return render_template('login.html', form_login=form_login)


# Página para envio de e-mail ao desenvolvedor, ainda em construção
@app.route("/enviar", methods=['GET', 'POST'])
def enviar():
    icongit = url_for('static', filename='images/github.png')
    iconface = url_for('static', filename='images/facebook.png')
    iconinst = url_for('static', filename='images/instagram.png')
    iconln = url_for('static', filename='images/linkedin.png')
    form_enviar = FormEnviarEmail()
    if 'botaoSubmitEnviar' in request.form:
        flash('E-mail enviado com sucesso!', 'alert-success')
        return redirect(url_for('/'))
    return render_template('enviar.html',
                           form_enviar=form_enviar,
                           icongit=icongit,
                           iconface=iconface,
                           iconln=iconln,
                           iconinst=iconinst)


# Página para edição e atualização de informações do perfil profissional
@app.route("/perfil", methods=['GET', 'POST'])
@login_required
def perfil():
    form_profissao = FormProfissao()
    form_habilidade = FormHabilidades()
    if 'botaoSubmitConfirmarProfissao' in request.form:
        if form_profissao.datafim.data != None:
            experiencia = Experiencias(cargo=form_profissao.cargo.data,
                                       entidade=form_profissao.entidade.data,
                                       dataadmin=datetime.strptime(str(form_profissao.dataadmin.data), '%Y-%m-%d'),
                                       datafim=datetime.strptime(str(form_profissao.datafim.data), '%Y-%m-%d'),
                                       atribuicao=form_profissao.atribuicao.data,
                                       conquistas=form_profissao.conquistas.data,
                                       profissional=current_user)
        else:
            experiencia = Experiencias(cargo=form_profissao.cargo.data,
                                       entidade=form_profissao.entidade.data,
                                       dataadmin=datetime.strptime(str(form_profissao.dataadmin.data), '%Y-%m-%d'),
                                       atribuicao=form_profissao.atribuicao.data,
                                       conquistas=form_profissao.conquistas.data,
                                       profissional=current_user)
        database.session.add(experiencia)
        database.session.commit()
        flash(f'Experiência profissional para a empresa {form_profissao.entidade.data} foi atualizada!', 'alert-success')
        return redirect(url_for('perfil'))
    if 'botaoSubmitConfirmarCurso' in request.form:
        if form_habilidade.certificado.data:
            nome_imagem = SalvarImagem(form_habilidade.certificado.data)
        else:
            nome_imagem = 'default.png'
        if form_habilidade.datafinal.data != None:
            habilidade = Habilidades(curso=form_habilidade.curso.data,
                                   tipo_curso=form_habilidade.tipo_curso.data,
                                   escola=form_habilidade.escola.data,
                                   dataini=datetime.strptime(str(form_habilidade.dataini.data), '%Y-%m-%d'),
                                   datafinal=datetime.strptime(str(form_habilidade.datafinal.data), '%Y-%m-%d'),
                                   competencia=form_habilidade.competencia.data,
                                   certificado=nome_imagem,
                                   profissional=current_user)
        else:
            habilidade = Habilidades(curso=form_habilidade.curso.data,
                                   tipo_curso=form_habilidade.tipo_curso.data,
                                   escola=form_habilidade.escola.data,
                                   dataini=datetime.strptime(str(form_habilidade.dataini.data), '%Y-%m-%d'),
                                   competencia=form_habilidade.competencia.data,
                                   certificado=nome_imagem,
                                   profissional=current_user)
        database.session.add(habilidade)
        database.session.commit()
        flash(f'Curso {form_habilidade.curso.data} foi atualizado!', 'alert-success')
        return redirect(url_for('perfil'))
    return render_template('perfil.html',
                           form_habilidade=form_habilidade,
                           form_profissao=form_profissao)


# Executar logaut
@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash(f'Logout realizado com sucesso, volte sempre!', 'alert-success')
    return redirect(url_for('home'))

# Pagina que cria a versão impressoa do curriculo. As habilidades serão apresentadas
#ordenadas por tipo de curso como na home, porém selecionando quantidades, então
#começará apresentando um do tipo Academico, depois três cursos do tipo especialização,
#depois um curso do tipo línguas, e as três ultimas experiencias profissionais. Sempre
#do mais atual ao mais antigo.
@app.route('/imprimir')
def imprimir():
    usuario1 = Usuario.query.filter_by(id=1).first()
    experiencias = Experiencias.query.order_by(Experiencias.dataadmin.desc())
    academicos = Habilidades.query.filter_by(tipo_curso='academico').order_by(Habilidades.dataini.desc())
    especializacoes = Habilidades.query.filter_by(tipo_curso='especializacao').order_by(Habilidades.dataini.desc())
    linguas = Habilidades.query.filter_by(tipo_curso='linguas').order_by(Habilidades.dataini.desc())
    return render_template('imprimir.html',
                           usuario1=usuario1,
                           experiencias=experiencias,
                           academicos=academicos,
                           especializacoes=especializacoes,
                           linguas=linguas)


# Paginas de edição de habilidades
@app.route('/editarhabilidade<habilidade_id>', methods=['GET', 'POST'])
@login_required
def editar_habilidade(habilidade_id):
    habilidade = Habilidades.query.get(habilidade_id)
    form_profissao = FormProfissao()
    form_habilidade = FormHabilidades()
    if request.method == 'POST' and 'botaoSubmitConfirmarCurso' in request.form:
        habilidade.curso = form_habilidade.curso.data
        habilidade.tipo_curso = form_habilidade.tipo_curso.data
        habilidade.escola = form_habilidade.escola.data
        habilidade.dataini=datetime.strptime(str(form_habilidade.dataini.data), '%Y-%m-%d')
        if form_habilidade.datafinal.data != None:
            habilidade.datafinal=datetime.strptime(str(form_habilidade.datafinal.data), '%Y-%m-%d')
        habilidade.competencia=form_habilidade.competencia.data
        if form_habilidade.certificado.data:
            nome_imagem = SalvarImagem(form_habilidade.certificado.data)
            habilidade.certificado = nome_imagem
        database.session.commit()
        flash(f'Dados do curso {form_habilidade.curso.data} atualizados com sucesso!', 'alert-success')
        return redirect(url_for('home'))
    elif request.method == "GET":
        form_habilidade.curso.data = habilidade.curso
        form_habilidade.tipo_curso.data = habilidade.tipo_curso
        form_habilidade.escola.data = habilidade.escola
        form_habilidade.dataini.data = habilidade.dataini
        form_habilidade.datafinal.data = habilidade.datafinal
        form_habilidade.competencia.data = habilidade.competencia
    if 'botaoSubmitConfirmarProfissao' in request.form:
        flash(f'Nenhuma profissão foi selecionada, tente novamente!', 'alert-danger')
        return redirect(url_for('home'))
    return render_template('editarhabilidades.html',
                           habilidade=habilidade,
                           form_habilidade=form_habilidade,
                           form_profissao=form_profissao)


# Paginas de edição de experiencias
@app.route('/editarprofissao<profissao_id>', methods=['GET', 'POST'])
@login_required
def editar_profissao(profissao_id):
    profissao = Experiencias.query.get(profissao_id)
    form_profissao = FormProfissao()
    form_habilidade = FormHabilidades()
    if request.method == 'POST' and 'botaoSubmitConfirmarCurso' in request.form:
        flash(f'Nenhum curso foi selecionado, tente novamente!', 'alert-danger')
        return redirect(url_for('/'))
    if 'botaoSubmitConfirmarProfissao' in request.form:
        profissao.cargo = form_profissao.cargo.data
        profissao.entidade = form_profissao.entidade.data
        profissao.dataadmin = datetime.strptime(str(form_profissao.dataadmin.data), '%Y-%m-%d')
        if form_profissao.datafim.data != None:
            profissao.datafim = datetime.strptime(str(form_profissao.datafim.data), '%Y-%m-%d')
        profissao.atribuicao = form_profissao.atribuicao.data
        profissao.conquistas = form_profissao.conquistas.data
        database.session.commit()
        flash(f'Dados de {form_profissao.entidade.data} atualizados com sucesso!', 'alert-success')
        return redirect(url_for('/'))
    elif request.method == "GET":
        form_profissao.cargo.data = profissao.cargo
        form_profissao.entidade.data = profissao.entidade
        form_profissao.dataadmin.data = profissao.dataadmin
        form_profissao.datafim.data = profissao.datafim
        form_profissao.atribuicao.data = profissao.atribuicao
        form_profissao.conquistas.data = profissao.conquistas
    return render_template('editarprofissao.html',
                           profissao=profissao,
                           form_habilidade=form_habilidade,
                           form_profissao=form_profissao)


# Paginas de exclusão de habilidades
@app.route('/editarhabilidade<habilidade_id>excluir', methods=['GET', 'POST'])
@login_required
def excluir_habilidade(habilidade_id):
    habilidade = Habilidades.query.get(habilidade_id)
    if current_user.is_authenticated:
        database.session.delete(habilidade)
        database.session.commit()
        flash('Registro de curso excluido com sucesso. Esta ação não pode ser retornada', 'alert-danger')
        return redirect(url_for('home'))
    else:
        abort(403)


# Paginas de edição de experiências
@app.route('/editarprofissao<profissao_id>excluir', methods=['GET', 'POST'])
@login_required
def excluir_profissao(profissao_id):
    profissao = Experiencias.query.get(profissao_id)
    if current_user.is_authenticated:
        database.session.delete(profissao)
        database.session.commit()
        flash('Registro de experiência excluido com sucesso. Esta ação não pode ser retornada', 'alert-danger')
        return redirect(url_for('home'))
    else:
        abort(403)

