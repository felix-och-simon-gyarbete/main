from my_server import app
from flask import render_template, request, redirect, url_for, flash, session, abort
from my_server.database_handler import create_connection

def is_logged_in():
    if 'logged_in' in session.keys() and session['logged_in']:
        return True
    else:
        return False
def get_user(username):
    conn = create_connection()
    cur = conn.cursor()
    users = cur.execute('SELECT * FROM users')
    conn.close()
    for user in users:
        if user[2] == username:
            return user
    return False
@ app.route('/')
@ app.route('/index')
def start():
    return render_template('index.html')

@ app.route('/login',  methods=['POST', 'GET'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    if request.method=='POST':
        conn = create_connection()
        cur = conn.cursor()
        users = cur.execute('SELECT * FROM users')
        
        username = request.form['username']
        password = request.form['password']
        
        for user in users:
            print(user)
            if user[2] == username and user[1] == password:
                session['logged_in'] = True
                session['username'] = username
                flash('Du är inloggad hej då', 'info')
                conn.close()
                return redirect(url_for('start'))

        abort(401)

@ app.route('/produkter')
def produkter():
    return render_template('produkter.html')



@ app.route('/varukorg')
def varukorg():
    return render_template('varukorg.html')

@ app.route('/newUser', methods=['POST', 'GET'])
def newUser():
    if request.method=='GET':
        return render_template('newUser.html')
    if request.method== 'POST':
        username = request.form['username']
        password = request.form['password']
        injection = (username, password, 0)
        sql = 'INSERT INTO users(username, password,admin) VALUES (?,?,?)'
        print(sql)
        conn = create_connection()
        cur = conn.cursor()
        cur.execute(sql, injection)
        conn.commit()
        conn.close()
        return redirect(url_for('login'))

@ app.route('/logout')
def loggaUt():
    session['logged_in'] = False
    session.pop('username', None)
    flash('Du är nu utloggad', 'info')
    return redirect(url_for('start'))
