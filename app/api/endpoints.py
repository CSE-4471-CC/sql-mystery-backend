from flask import Flask, Blueprint, request, jsonify;
from app.db import get_db
from app.helper import *

# lines 5-33 written by Lia Ferguson
bp = Blueprint('endpoints', __name__, url_prefix='/endpoints')


# endpoint for Step 1 SQL Injection Task 
@bp.route('/login_bypass', methods = ['POST'])
def login_bypass():
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

@bp.route('/login_query', methods = ['POST'])
def login_query():
	database = get_db()

	user_id = request.get_json()['user_id']
	password = request.get_json()['password']
	game_step = request.get_json()['game_step']

	quote = ""
	if user_id.find("\"") == -1 and user_id.find('\'') == -1:
		user_id = "\"" + user_id + "\""
		password = "\"" + password + "\""
	elif user_id.find('\'') != -1:
		quote = "\'"
	else:
		quote = "\""
	
	login_q = 'SELECT * FROM USERS WHERE User_ID = {quote}{u_id} AND Password = {quote}{pwd}'.format(quote=quote, u_id = user_id, pwd = password)

	commands = login_q.split(";", -1)
	all_query_results = []
	formatted_query_results = []
	error = ''
	try:
		for command in commands:
			query_results = database.execute(command).fetchall()
			all_query_results.append(query_results)
	except Exception as e:
		error = e.args

	if error == '':
		table_columns = queried_table_columns(commands[1])
		print(table_columns)
		formatted_query_results = format_query_results(all_query_results[1], table_columns)
		match_expected_results = check_expected_results(all_query_results[1], game_step)
	if len(formatted_query_results) > 0 :
		if match_expected_results:
			response = {
				'isQuerySuccessful': 'true',
				'correctResults': 'true',
				'results': formatted_query_results,
				'error': ''
			}
		else: 
			response = {
				'isQuerySuccessful': 'true',
				'correctResults': 'false',
				'results': formatted_query_results,
				'error': 'SQL Query was valid but it doesn\'t return the information that you need!'
			}
	else:
		error = error if error != '' else 'SQL Query was valid but there were no matching records returned.'
		response = {
			'isQuerySuccessful': 'false',
			'correctResults': 'false',
			'results': '',
			'error': error
		}

	print(response)
	return jsonify(response)



