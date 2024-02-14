import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')




@bp.route('/registro', methods=('GET', 'POST'))
def registro():
    if request.method == 'POST':
        nome_usuario = request.form['nome_usuario']
        senha = request.form['senha']
        db = get_db()
        error = None

        if not nome_usuario:
            error = 'É preciso um usuário.'
        elif not senha:
            error = 'É preciso uma senha'
        if error is None:
            try:
                db.execute(
                    "INSERT INTO usuario (nome_usuario, senha) VALUES (?, ?)",
                    (nome_usuario, generate_password_hash(senha)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"Usuário {nome_usuario} já possui registro."
            else:
                return redirect(url_for("auth.login"))
        flash(error)
    return render_template('auth/register.html')





@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        nome_usuario = request.form['nome_usuario']
        senha = request.form['senha']
        db = get_db()
        error = None
        usuario = db.execute('SELECT * FROM usuario WHERE nome_usuario = ?', (nome_usuario,)).fetchone()
    
        if usuario is None:
            error = 'Usuário não consta'
        elif not check_password_hash(usuario['senha'], senha):
            error = 'Senha incorreta'

        if error is None:
            session.clear()
            session['usuario_id'] = usuario['id']
            return redirect(url_for('index'))
    
        flash(error)

    return render_template('auth/login.html')




@bp.before_app_request
def usuario_logado():
    usuario_id = session.get('usuario_id')

    if usuario_id is None:
        g.usuario = None
    else:
        g.usuario = get_db().execute('SELECT * FROM usuario WHERE id = ?', (usuario_id,)).fetchone




@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))



def requisitos_login(view):
    @functools.wraps(view)
    def view_wrapped(**kwargs):
        if g.usuario is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return view_wrapped