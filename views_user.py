from flask import (
    flash, 
    redirect, 
    render_template, 
    request, 
    session, 
    url_for, 
)

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
    if usuario:
        if form.senha.data == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logado com sucesso!')
            # O parm. proxima_pagina não está no FlaskForm.
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
        # O código faltante na aula.
        flash('Senha inválida.')
        return redirect(url_for('login'))
        # Fim do código faltante.
    else:
        flash('Usuário não logado.')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('index'))
