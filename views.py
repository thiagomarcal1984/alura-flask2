from flask import (
    flash, 
    redirect, 
    render_template, 
    request, 
    send_from_directory,
    session, 
    url_for, 
)
from jogoteca import app, db
from models import Jogos, Usuarios

from helpers import recupera_imagem, deleta_arquivo
import time

@app.route('/')
def index():
    lista = Jogos.query.order_by(Jogos.id.asc())
    return render_template('lista.html', titulo='Jogos', jogos=lista)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Jogo')

@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogos.query.filter_by(nome=nome).first()

    if jogo:
        flash('Jogo já existente!')
        return redirect(url_for('index'))

    novo_jogo = Jogos(nome=nome, categoria=categoria, console=console)
    db.session.add(novo_jogo)
    db.session.commit()
    # db.session.refresh(novo_jogo) # Atualizar o objeto para buscar o ID.
    
    arquivo = request.files.get('arquivo')
    upload_path = app.config.get('UPLOAD_PATH')
    timestamp = time.time()
    arquivo.save(f'{upload_path}/capa-{novo_jogo.id}-{timestamp}.jpg')

    return redirect(url_for('index'))

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar')))
        # Sem o código do comentário abaixo, a próxima URL fica mal formada.
        # return redirect(url_for('login', proxima=url_for('editar', id=id)))

    jogo = Jogos.query.filter_by(id=id).first()

    contexto = {
        'titulo': 'Editando Jogo', 
        'jogo': jogo,
        'capa_jogo': recupera_imagem(id),
    }
    # Os dois asteriscos são o spread-operator do Python.
    return render_template('editar.html', **contexto)

@app.route('/atualizar', methods=['POST',])
def atualizar():
    id = request.form.get('id') # Vem do campo oculto do template.
    jogo = Jogos.query.filter_by(id=id).first()
    jogo.nome = request.form.get('nome')
    jogo.categoria = request.form.get('categoria')
    jogo.console = request.form.get('console')

    # db.session.add(jogo) # Este comando não foi necessário pra atualizar.
    db.session.commit()

    arquivo = request.files.get('arquivo')
    upload_path = app.config.get('UPLOAD_PATH')
    timestamp = time.time()
    deleta_arquivo(jogo.id)
    arquivo.save(f'{upload_path}/capa-{jogo.id}-{timestamp}.jpg')

    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))

    Jogos.query.filter_by(id=id).delete()
    db.session.commit()
    deleta_arquivo(id)
    flash('Jogo deletado com sucesso!')
    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    usuario = Usuarios.query.filter_by(nickname=request.form['usuario']).first()
    if usuario:
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Usuário não logado.')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('index'))

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory(app.config.get('UPLOAD_PATH'), nome_arquivo)
