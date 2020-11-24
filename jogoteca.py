from flask import Flask, render_template, request, redirect, session, flash, url_for
from models import Jogo, Usuario
from dao import JogoDao, UsuarioDao
import mysql.connector

app = Flask(__name__)
app.secret_key = 'alura'

db = mysql.connector.connect(
    host="localhost",
    user="jaison",
    port = 3306,
    password="119954/-Jac",
    database = "jogoteca",
    auth_plugin='mysql_native_password'
)

jogo_dao = JogoDao(db)
usuario_dao = UsuarioDao(db)

'''
usuario1 = Usuario('luan', 'Luan Marques', '1234')
usuario2 = Usuario('Nico', 'Nico Steppat', '7a1')
usuario3 = Usuario('flavio', 'flavio Almeida', 'javascript')

usuarios = {usuario1.id: usuario1,
            usuario2.id: usuario2,
            usuario3.id: usuario3}

jogo1 = Jogo('Super Mario', 'Ação', 'SNES')
jogo2 = Jogo('Pokemon Gold', 'RPG', 'GBA')

lista = [jogo1, jogo2]
'''

@app.route('/')
def index():
    lista = jogo_dao.listar()
    return render_template('lista.html', titulo='Jogos',
                           jogos=lista)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Jogo')

@app.route('/criar', methods=['POST',])
def criar():
    nome = request. form['nome']
    categoria = request. form['categoria']
    console = request. form['console']
    jogo = Jogo(nome, categoria, console)
    jogo_dao.salvar(jogo)
    return redirect(url_for('index'))


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)


@app.route('/autenticar', methods=['POST', ])
def autenticar():
    usuario = usuario_dao.busca_por_id(request.form['usuario'])
    if usuario:
        if usuario.senha == request.form['senha']:
            session['usuario_logado'] = usuario.id
            flash(usuario.nome + ' logou com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Não logado, tente novamente!')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuário logado!')
    return redirect(url_for('index'))


app.run(debug=True)
