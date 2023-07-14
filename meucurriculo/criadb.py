from meucurriculo import app, database
from meucurriculo.models import Usuario, Habilidades, Experiencias

"""
---------------Arquivo de criação de banco de dados------------------

    Este arquivo tem a função de criar o arquivo de banco de dados 
curriculo.db. Ele não temuma integração direta com os demais arquivos, 
sendo executado de forma separada e apenas uma vez.
    Garanta que todos os outros arquivos do projeto estejam fechados e
procure rodar o criadb.py de forma que ele não realize qualquer chama-
da para outros arquivos do projeto.
    DICA - No PyCharm, clique em Run / Debuig Configuration e rode na 
opção Currente File.

-----------------------Observações importantes------------------------

    O primeiro bloco deste arquivo cria o banco de dados e suas tabelas
configuradas de acordo com a estrutura do models.py.
    O segundo bloco instancia um objeto usuário na tabela Usuario.
    O terceiro bloco é apenas um teste para confirmar que a instancia 
do objeto usuário foi criada com sucesso.
    Perceba que o site não permitirá cadastrar novos usuários, mas per-
mitirá editar as informações do unico usuário existente.
    A finalidade desta aplicação é exatamente esta, permitir que apenas 
um usuário tenha seu curriculo cadastrado e rodando online.  
    O usuário criado nesta instancia é apenas inicial.
    No final desta rotina existe um trecho comentado para deletar o 
banco de dados caso seja nescessário. Para usar, basta descomentar.
_______________________________________________________________________

"""

with app.app_context():
    database.create_all()

with app.app_context():
    usuario1 = Usuario(
        username = 'UserNick',
        senha = '$2b$12$WJXkqsSvWrihzNHlfAvyouqj.GuYtt0YwoG6.E8fE2BAmMAlaKNqK',
        firstname = 'Novo',
        lastname = 'Usuário',
        profissao = 'Profissão',
        logradouro = 'Rua Nome da Rua, 001',
        bairro = 'Nome do Bairro',
        cidade = 'Nome da Cidade',
        uf = 'UF',
        cep = '12345678',
        email = 'email@dominio.com',
        fone = '(11) 9 9999-9999',
        github = '#',
        linkedin = '#',
        facebook = '#',
        instagran = '#',
        objetivo = 'Digitar um resumo de seus objetivos',
        competencias = 'Digitar um resumo de suas competencias',
        foto_perfil = 'default.jpg',
        qrcode = 'default.jpg'
    )
    database.session.add(usuario1)
    database.session.commit()

with app.app_context():
    meu_usuario = Usuario.query.all()
    print(meu_usuario)

# with app.app_context():
#     meu_usuario = Usuario.query.filter_by().first()
#     print(meu_usuario.senha)
#     print(meu_usuario.username)

# with app.app_context():
#     database.drop_all()
#     database.create_all()
