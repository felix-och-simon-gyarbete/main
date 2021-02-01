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
conn.commit()
