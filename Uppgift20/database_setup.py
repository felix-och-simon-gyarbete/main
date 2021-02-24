from my_server.database_handler import create_connection

conn = create_connection()
cur = conn.cursor()
sql = '''CREATE TABLE IF NOT EXISTS users(
		user_id INTEGER PRIMARY KEY,
		password TEXT NOT NULL,
		username TEXT NOT NULL,
		admin INTEGER NOT NULL
		)'''

cur.execute(sql)
sql = '''CREATE TABLE IF NOT EXISTS produkter(
		produkt_id INTEGER PRIMARY KEY,
		namn TEXT NOT NULL,
		pris REAL NOT NULL, 
		beskrivning TEXT NOT NULL
		)'''
cur.execute(sql)
sql = '''CREATE TABLE IF NOT EXISTS har(
		produkt_id INTEGER REFERENCES produkter(produkt_id),
		user_id INTEGER REFERENCES users(user_id)
		)'''
cur.execute(sql)
lista = [('Hamburgare', 10, "Jävligt god"), ('Cheese', 5, "Rätt schysst"), ( 'Bantningsmedel', 100, "Inte för alla"), ( 'Tjockisar', 20, "Väldigt tjocka"), ('Dampbarn',19 , "dampiga som fan"), ('Chonksel', 0, "ta med släp när ni hämtar")]
cur.executemany("INSERT INTO produkter(namn, pris, beskrivning) VALUES (?,?,?)", lista)
cur.execute('INSERT INTO users(password, username, admin) VALUES (?, ?, ?)', ('admin', 'admin', 1))
conn.commit()
