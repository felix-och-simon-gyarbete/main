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
            if user[2] == username and user[1] == password:
                session['logged_in'] = True
                session['username'] = username
                session['user_id'] = get_user(username)[0]
                flash('Du är inloggad hej då', 'info')
                conn.close()
                return redirect(url_for('start'))

        abort(401)

@ app.route('/produkter')
def produkter():
    conn = create_connection()
    cur = conn.cursor()
    sql = "SELECT * FROM produkter"
    rows = cur.execute(sql)
    return render_template('produkter.html', rows = rows)

@ app.route('/lagg_till/<produkt_id>')
def laggTillProdukt(produkt_id=""):
    if not is_logged_in():
        flash("Du måste logga in för att lägga till produkter i varukorgen", 'info')
        return redirect(url_for('login'))
    produkt_id = int(produkt_id)
    conn = create_connection()
    cur = conn.cursor()
    username = session['username']
    user_id = get_user(username)[0]
    sql = 'SELECT * FROM produkter WHERE produkt_id = (?)'
    cur.execute(sql, (user_id,))
    sql = "INSERT INTO har(produkt_id, user_id) VALUES (?,?)"
    injection = (produkt_id, user_id)
    cur.execute(sql, injection)
    sql = 'SELECT namn FROM produkter WHERE produkt_id = (?)'
    cur.execute(sql, (produkt_id,))
    produkt_namn = cur.fetchone()
    produkt_namn = "".join(produkt_namn)
    conn.commit()
    flash(f"Produkten {produkt_namn} har lagts till i varukorgen", "info")
    return redirect(url_for('produkter'))

@ app.route('/varukorg')
def varukorg():
    user_id  = get_user(session['username'])[0]
    sql = 'SELECT produkter.produkt_id, produkter.namn, produkter.pris, count(*) FROM har, produkter WHERE produkter.produkt_id = har.produkt_id AND har.user_id = (?) GROUP BY produkter.namn'
    conn = create_connection()
    cur = conn.cursor()
    products = cur.execute(sql, (user_id,)).fetchall()
    total = cur.execute('SELECT SUM(pris) FROM har, produkter WHERE produkter.produkt_id = har.produkt_id AND har.user_id = (?)', (user_id,)).fetchone()[0]
    total = int(total)
    antal = cur.execute('SELECT COUNT(*) FROM har, produkter WHERE produkter.produkt_id = har.produkt_id AND har.user_id = (?)', (user_id,)).fetchone()[0]
    return render_template('varukorg.html', products = products, total = total, antal = antal)

@ app.route('/newUser', methods=['POST', 'GET'])
def newUser():
    if request.method=='GET':
        return render_template('newUser.html')
    if request.method== 'POST':
        username = request.form['username']
        password = request.form['password']
        injection = (username, password, 0)
        sql = 'INSERT INTO users(username, password,admin) VALUES (?,?,?)'
        conn = create_connection()
        cur = conn.cursor()
        cur.execute(sql, injection)
        conn.commit()
        conn.close()
        return redirect(url_for('login'))

@ app.route('/delete', methods=['POST'])
def delete():
    conn = create_connection()
    cur = conn.cursor()
    id = request.form['id']
    id = int(id)
    sql = "DELETE FROM har WHERE produkt_id = (?) AND user_id = (?)"
    user_id = session['user_id']
    print(f"Produkt id: {id}  user_id: {user_id}")
    injection = (id, user_id)
    print(injection)
    cur.execute(sql, injection)
    conn.commit()
    return redirect(url_for('varukorg'))

@ app.route('/logout')
def loggaUt():
    session['logged_in'] = False
    session.pop('username', None)
    flash('Du är nu utloggad', 'info')
    return redirect(url_for('start'))
