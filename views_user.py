from flask import (
    flash, 
    redirect, 
    render_template, 
    request, 
    session, 
    url_for, 
)

from flask_bcrypt import check_password_hash

from jogoteca import app
from models import Usuarios
from helpers import FormularioUsuario

@app.route('/login')
def login():
    contexto = {
        'proxima' : request.args.get('proxima'),
        'form' : FormularioUsuario(),
    }
    return render_template('login.html', **contexto)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    form = FormularioUsuario(request.form)
    usuario = Usuarios.query.filter_by(nickname=form.nickname.data).first()
    senha = check_password_hash(usuario.senha, form.senha.data)
    if usuario and senha:
        session['usuario_logado'] = usuario.nickname
        flash(usuario.nickname + ' logado com sucesso!')
        # O parm. proxima_pagina não está no FlaskForm.
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
