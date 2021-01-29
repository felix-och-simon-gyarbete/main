from my_server import app
from flask import render_template, request, redirect, url_for, flash, session, abort
from my_server.hardcoded_database import users, posts
def is_logged_in():
    if 'logged_in' in session.keys() and session['logged_in']:
        return True
    else:
        return False
def get_user(username):
    for user in users:
        if user['username'] == username:
            return user
    return False
@ app.route('/')
@ app.route('/index')
def start():
    print(users)
    return render_template('index.html')
@ app.route('/login',  methods=['POST', 'GET'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        for user in users:
            if user['username'] == username and user['password'] == password:
                session['logged_in'] = True
                session['username'] = username
                flash('Du är inloggad hej då', 'info')
                return redirect(url_for('start'))
        abort(401)

@ app.route('/produkter')
def produkter():
    return render_template('produkter.html')



@ app.route('/varukorg')
def varukorg():
    return render_template('varukorg.html')




@ app.route('/logout')
def loggaUt():
    session['logged_in'] = False
    session.pop('username', None)
    flash('Du är nu utloggad', 'info')
    return redirect(url_for('start'))
