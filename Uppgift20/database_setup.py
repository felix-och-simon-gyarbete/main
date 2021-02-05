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
sql = '''CREATE TABLE IF NOT EXISTS varukorg(
		user_id INTEGER REFERENCES users(user_id),
		produkt_id INTEGER REFERENCES produkter(produkt_id)
		)'''
cur.execute(sql)
sql = '''CREATE TABLE IF NOT EXISTS produkter(
		produkt_id INTEGER PRIMARY KEY,
		namn TEXT NOT NULL,
		pris REAL NOT NULL, 
		beskrivning TEXT NOT NULL
		)'''
cur.execute(sql)
lista = [(1, 'Hamburgare', 10, "Jävligt god"), (2, 'Cheese', 5, "Rätt schysst"), (3, 'Bantningsmedel', 100, "Inte för alla"), (4, 'Tjockisar', 20, "Väldigt tjocka"),(5, 'Dampbarn',19 , "dampiga som fan"), (6, 'Chonksel', 0, "ta med släp när ni hämtar"),]
cur.executemany("INSERT INTO produkter VALUES (?,?,?)", lista)

conn.commit()
