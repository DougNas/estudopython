from meucurriculo import app

"""
-----------Aplicação para criação de site: Curriculo online----------

    Objetivo - Criação de site de curriculo online para consolidação
de conhecimentos de desenvolvimento de site utilizando linguagem 
Python.
    Utilização de biblioteca flask para funcionabilidade do site e da
biblioteca sqlalchemy para trabalho com banco de dados.

----------------------Funcionabilidades do site----------------------

    Permitir a criação de um usuário, permitir que este usuário possa 
editar seu dados pessoais e de contato, permitir que o usuário possa 
atualizar ou incluir novos conhecimentos e abilidades, permitir que o
usuário possa atualizar ou incluir novas experiências profissionais,
permitir que visitantes possam conferir as informações do usuário, 
permitir que visitantes possam enviar e-mail do proprio site para o 
desenvolvedor e por fim, imprimir uma versão impressa do corriculo. 

----------------------Bibliotecas nescessárias-----------------------

flask
flask-wtf
email_validator
flask-sqlalchemy
flask-bcrypt
flask-login
Pillow
    
Link para importação do Bootstrap => https://getbootstrap.com/docs/5.3/getting-started/download/
_____________________________________________________________________
"""

if __name__ == '__main__':
    app.run(debug=True)
