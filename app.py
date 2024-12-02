import sqlite3
from flask import Flask, jsonify, request
import traceback

app = Flask(__name__)

DATABASE = 'points.db'

def connect_to_database():
	return sqlite3.connect(DATABASE)

#Adds a specific points transaction to the database, storing the timestamp, 
#payer, and the number of points
@app.route('/add', methods=['POST'])
def add():
	#getting the cursor for the DB
	conn = connect_to_database()
	cursor = conn.cursor()

	#try-except
	try:
		data = request.get_json()

		#grabbing info
		payer = data['payer']
		points = int(data['points'])
		timestamp = data['timestamp']

		#inserting the data into the TRANSACTIONS table
		cursor.execute("INSERT INTO TRANSACTIONS (PAYER, POINTS, TIMESTAMP) VALUES (?, ?, ?)", (payer, points, timestamp,))
		conn.commit()
		conn.close()

		return "Success", 200

	except Exception:
		conn.close()
		return "Failure", 400

#Let's the user spend the points (based on the criteria provided)
@app.route('/spend', methods=['POST'])
def spend():
	#getting the cursor for the DB
	conn = connect_to_database()
	cursor = conn.cursor()

	#try-except
	try:
		data = request.get_json()

		#grabbing the number of points to spend
		points_needed = int(data['points'])

		#get the total number of points the user has
		cursor.execute('SELECT SUM(POINTS) as total FROM TRANSACTIONS')
		total = cursor.fetchone()[0]
		#if the total the user has is less than the amount being spent, we return 400 (error)
		if total is None or total < points_needed:
			return "User doesn't have enough points!", 400

		#get each payer's current balance to ensure none fall below 0
		cursor.execute('SELECT PAYER, SUM(POINTS) as balance FROM TRANSACTIONS GROUP BY PAYER')
		balances = {}
		#looping through and adding the balance to each payer
		for row in cursor.fetchall():
		    payer = row[0]
		    balance = row[1]
		    balances[payer] = balance


		#if enough points, we fetch all transactions in reverse order by timestamp (oldest first)
		cursor.execute('SELECT * FROM TRANSACTIONS ORDER BY TIMESTAMP ASC')
		txns = cursor.fetchall()

		payer_tracker = dict() #track the points deducted from each payer
		#looping through each transactions
		for txn in txns:
			#break loop if we have the points
			if points_needed == 0:
				break

			#get the info
			print(txn)
			_id = txn[0]
			payer = txn[1]
			pts = int(txn[2])

			deduct = min(pts, points_needed) #don't deduct more points than needed

			#checking if the deduction would cause the payer's balance to go below 0
			if balances[payer] - deduct  < 0:
				#limit deducted amount to ensure balance stays at or above 0
				deduct = balances[payer]

			balances[payer] -= deduct
			points_needed -= deduct

			#adding the payer to the tracker
			if payer not in payer_tracker:
				payer_tracker[payer] =  (0 - deduct)
			else:
				payer_tracker[payer] -= deduct

			#updating the transaction table in the DB
			cursor.execute("UPDATE TRANSACTIONS SET POINTS = POINTS - ? WHERE ID = ?", (deduct, _id,))
			conn.commit()

		conn.close()
		#summarizing the JSON data to send
		result = [] #return list

		for key, value in payer_tracker.items():
		    result.append({"payer": key, "points": value})

		return jsonify(result), 200


	except Exception as e:
		conn.close()
		return "Failure", 400


#Get the points by payer
@app.route('/balance', methods=['GET'])
def balance():
	#getting the cursor for the DB
	conn = connect_to_database()
	cursor = conn.cursor()

	#try-except
	try:

		#adding up and grouping each payer's points from transactions
		cursor.execute('SELECT PAYER, SUM(POINTS) as balance FROM TRANSACTIONS GROUP BY PAYER')
		result = cursor.fetchall()

		#response object
		balances = {}
		for row in result:
			payer = row[0]
			balance = row[1]
			balances[payer] = balance

		conn.close()
		return jsonify(balances), 200

	except Exception:
		print(traceback.print_exc())
		conn.close()
		return "Failure", 400

if __name__ == '__main__':
	app.run(debug=True, port=8000)















