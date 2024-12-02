import sqlite3

connection = sqlite3.connect('points.db')
cursor = connection.cursor()

cursor.execute('''
	CREATE TABLE IF NOT EXISTS TRANSACTIONS
	(
		ID INTEGER PRIMARY KEY AUTOINCREMENT,
		PAYER TEXT,
		POINTS INT,
		TIMESTAMP DATEIMTE
	) 
	''')

connection.commit()
connection.close()