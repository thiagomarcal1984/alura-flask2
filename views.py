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

from helpers import recupera_imagem, deleta_arquivo, FormularioJogo
import time

@app.route('/')
def index():
    lista = Jogos.query.order_by(Jogos.id.asc())
    return render_template('lista.html', titulo='Jogos', jogos=lista)

@app.route('/novo')
def novo():
    form = FormularioJogo()
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    contexto = {
        'titulo' : 'Novo Jogo',
        'form' : form,
    }
    # Os dois asteriscos são o spread-operator do Python.
    return render_template('novo.html', **contexto)

@app.route('/criar', methods=['POST',])
def criar():
    form = FormularioJogo(request.form)
    if not form.validate_on_submit():
        return redirect(url_for('novo'))

    nome = form.nome.data
    categoria = form.categoria.data
    console = form.console.data

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
    form = FormularioJogo(
        nome=jogo.nome,
        categoria=jogo.categoria,
        console=jogo.console,
    )

    contexto = {
        'titulo': 'Editando Jogo', 
        'id': id, # Não é mais necessário enviar o jogo.
        'capa_jogo': recupera_imagem(id),
        'form': form, # O formulário substitui o jogo.
    }
    # Os dois asteriscos são o spread-operator do Python.
    return render_template('editar.html', **contexto)

@app.route('/atualizar', methods=['POST',])
def atualizar():
    form = FormularioJogo(request.form)

    if form.validate_on_submit():
        jogo = Jogos.query.filter_by(id=request.form.get('id')).first()
        jogo.nome = form.nome.data
        jogo.categoria = form.categoria.data
        jogo.console = form.console.data

        # db.session.add(jogo) # Este comando não foi necessário pra atualizar.
        db.session.commit()

        arquivo = request.files.get('arquivo')
        upload_path = app.config.get('UPLOAD_PATH')
        timestamp = time.time()
        deleta_arquivo(jogo.id)
        arquivo.save(f'{upload_path}/capa-{jogo.id}-{timestamp}.jpg')

        return redirect(url_for('index'))
    return redirect(url_for('editar', id=request.form.get('id')))

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
