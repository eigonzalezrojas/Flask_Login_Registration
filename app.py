from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from decouple import config
import pymysql
import re
from werkzeug.security import check_password_hash  # Para verificar la contraseña hasheada

app = Flask(__name__)


app.secret_key = 'SECRETKEYAPP'

# Configuración de la base de datos
db = pymysql.connect(
    host="MYSQLHOST",
    user="MYSQLUSER",
    password="MYSQLPASSWORD",
    database="MYSQLDBNAME",
    cursorclass=pymysql.cursors.DictCursor
)

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        
        # Conexión a la base de datos usando pymysql
        with db.cursor() as cursor:
            # Consulta para obtener la cuenta por nombre de usuario
            cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
            account = cursor.fetchone()
        
        if account and check_password_hash(account['password'], password):
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully!'
            return render_template('index.html', msg=msg)
        else:
            msg = 'Incorrect username / password!'
    return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('username', None)
	return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        with db.cursor() as cursor:
            cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
            account = cursor.fetchone()
        
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Insertar el nuevo usuario con la contraseña hasheada
            with db.cursor() as cursor:
                hashed_password = generate_password_hash(password)                
                cursor.execute('INSERT INTO accounts (username, password, email) VALUES (%s, %s, %s)', (username, hashed_password, email))
                db.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('register.html', msg=msg)