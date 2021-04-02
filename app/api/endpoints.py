from flask import Flask, Blueprint, request, jsonify;
from app.db import get_db

# lines 5-33 written by Lia Ferguson
bp = Blueprint('endpoints', __name__, url_prefix='/endpoints')

NUM_RECORDS_USERS_TABLE = 7 # replace this number with actual number of records in database

# endpoint for Step 1 SQL Injection Task 
@bp.route('/login_query', methods = ['POST'])
def login_query():
	database = get_db()

	user_id = request.get_json()['user_id']
	password = request.get_json()['password']
	# wrong way to compose SQL query based on secure coding practices
	# this allows for SQL Injection to occur
	quote = ""
	if user_id.find("\"") == -1 and user_id.find('\'') == -1:
		user_id = "\"" + user_id + "\""
		password = "\"" + password + "\""
	elif user_id.find('\'') != -1:
		quote = "\'"
	else:
		quote = "\""
	
	login_q = 'SELECT * FROM USERS WHERE User_ID = {quote}{u_id} AND Password = {pwd}'.format(quote=quote, u_id = user_id, pwd = password)

	query_result = database.execute(login_q).fetchall()
	response = {}
	if len(query_result) == NUM_RECORDS_USERS_TABLE:
		response = {
			'isQuerySuccessful': 'true',
			'status': 'SUCCESS',
			'message': 'Congratulations! You successfully used SQL Injection to bypass authentication.'
		}

	else:
		response = {
			'isQuerySuccessful': 'false',
			'status': 'ERROR',
			'message': 'SQL Injection was not successful, please try again.'
		}
	print(response)
	print(user_id)
	return jsonify(response)



