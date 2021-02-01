import sqlite3

DB_PATH = 'my_db.db'

def create_connection(databas = DB_PATH):
	conn = None
	try:
		conn = sqlite3.connect(databas)
	except sqlite3.Error as e:
		print(e)
	return conn	