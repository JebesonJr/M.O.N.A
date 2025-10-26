# mona3.py
import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from database import init_db, create_account, get_account_by_username, list_accounts, approve_account, reject_account, validate_by_code

# Config
ADMIN_USER = os.environ.get('MONA_ADMIN_USER', 'Lord Over')
ADMIN_PASS = os.environ.get('MONA_ADMIN_PASS', '@Brasil1248')
ADMIN_PASS_HASH = generate_password_hash(ADMIN_PASS)
SECRET_KEY = os.environ.get('MONA_SECRET_KEY', 'change_this_secret')

app = Flask(__name__)
app.secret_key = SECRET_KEY

# Init DB on start
init_db()

# Routes
@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username').strip()
        email = request.form.get('email').strip()
        password = request.form.get('password')
        if not username or not email:
            flash('Usuário e email são obrigatórios.')
            return redirect(url_for('register'))
        existing = get_account_by_username(username)
        if existing:
            flash('Usuário já existe.')
            return redirect(url_for('register'))
        code = create_account(username, email, password)
        if not code:
            flash('Erro ao criar conta (usuário pode existir).')
            return redirect(url_for('register'))
        flash('Cadastro enviado. Aguarde aprovação do administrador.')
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/validate', methods=['GET', 'POST'])
def validate():
    if request.method == 'POST':
        code = request.form.get('code').strip()
        ok, res = validate_by_code(code)
        if ok:
            flash('Conta validada. Bem vindo ao sistema da Mente Operacional Neural Autônoma')
            return redirect(url_for('index'))
        else:
            flash(res)
            return redirect(url_for('validate'))
    return render_template('validate.html')

# Admin
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == ADMIN_USER and check_password_hash(ADMIN_PASS_HASH, password):
            session['admin_logged_in'] = True
            session['admin_user'] = ADMIN_USER
            return redirect(url_for('admin_panel'))
        else:
            flash('Usuário ou senha incorretos.')
            return redirect(url_for('admin_login'))
    return render_template('admin_login.html', default_user=ADMIN_USER)

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    session.pop('admin_user', None)
    flash('Logout realizado.')
    return redirect(url_for('index'))

from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin_logged_in'):
            flash('Você precisa fazer login como admin.')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated

@app.route('/admin/panel')
@login_required
def admin_panel():
    status = request.args.get('status')
    accounts = list_accounts(status)
    return render_template('admin_panel.html', accounts=accounts, admin_user=ADMIN_USER)

@app.route('/admin/approve', methods=['POST'])
@login_required
def admin_approve():
    acc_id = int(request.form.get('id'))
    note = request.form.get('note','')
    row = approve_account(acc_id, note)
    if row:
        validation_code = row['validation_code']
        # you can implement email sending here
        flash(f'Conta aprovada. Código de validação: {validation_code}')
    return redirect(url_for('admin_panel'))

@app.route('/admin/reject', methods=['POST'])
@login_required
def admin_reject():
    acc_id = int(request.form.get('id'))
    note = request.form.get('note','')
    reject_account(acc_id, note)
    flash('Conta rejeitada.')
    return redirect(url_for('admin_panel'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))