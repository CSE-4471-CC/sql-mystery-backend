from flask import Flask, Blueprint, request, jsonify;
from app.db import get_db
from app.helper import *

# lines 5-33 written by Lia Ferguson

NUM_RECORDS_USERS_TABLE = 8

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

# endpoint for all SQL Injection after step 1
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
		formatted_query_results = format_query_results(all_query_results[1], table_columns, game_step)
		match_expected_results = check_expected_results(all_query_results[1], game_step)
	if len(formatted_query_results) > 0:
		if match_expected_results:
			print_results_to_file(formatted_query_results, game_step)
			response = {
				'isQuerySuccessful': 'true',
				'correctResults': 'true',
				'results': formatted_query_results,
				'error': ''
			}
		else: 
			if len(table_columns) > len(CORRECT_RESULTS[game_step][0]):
				error = 'SQL Query returns too much information. Follow the directions and be more specific!'
			else:
				error = 'SQL Query was valid but it doesn\'t return the information that you need!'
			response = {
				'isQuerySuccessful': 'true',
				'correctResults': 'false',
				'results': formatted_query_results,
				'error': error
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

# endpoint to trigger trojan horse process in step 5
@bp.route('/trojan_horse', methods = ['POST'])
def trojan_horse():
	first_name = request.get_json()['first_name']
	last_name = request.get_json()['last_name']

	if first_name == '':
		response = {
			'isSuccess': 'false',
			'message': 'first name must be provided in order to proceed'
		}
	elif last_name == '':
		response = {
			'isSuccess': 'false',
			'message': 'last name must be provided in order to proceed'
		}
	else:
		execute_trojan_horse(first_name, last_name)

		response = {
			'isSuccess': 'true',
			'message': 'Just a moment! Loading...'
		}

	jsonify(response)
	return response

# endpoint that processes submission of suspect guesses
@bp.route('/suspect', methods = ['POST'])
def suspect():
	name = request.get_json()['name']
	game_step = request.get_json()['game_step']

	correct = check_suspect(name, game_step)
	

	response = {}
	if correct:
		print_results_to_file(name, game_step)
		response = {
			'correct': 'true',
			'message': 'The evidence suggests that this person is a suspect.'
		}
	else:
		response = {
			'correct': 'false',
			'message': 'There isn\'t enough evidence for this person to be a suspect.'
		}		

	jsonify(response)
	return response

# endpoint that processes normal login in final step of the game
@bp.route('/login', methods = ['POST'])
def login():
	database = get_db()

	user_id = request.get_json()['user_id']
	password = request.get_json()['password']
	response = {}
	if user_id == '':
		response = {
			'isLoginSuccessful': 'false',
			'error': 'You must provide a username'
		}
	elif password == '':
		response = {
			'isLoginSuccessful': 'false',
			'error': 'You must provide a password'
		}

	quote = ""
	formatted_password = ''
	if user_id.find("\"") == -1 and user_id.find('\'') == -1:
		user_id = "\"" + user_id + "\""
		formatted_password = "\"" + password + "\""
	elif user_id.find('\'') != -1:
		quote = "\'"
	else:
		quote = "\""
	
	login_q = 'SELECT * FROM USERS WHERE User_ID = {quote}{u_id}'.format(quote=quote, u_id = user_id)
	query_result = database.execute(login_q).fetchone()
	record = tuple(y for y in query_result)
	print(record)
	if len(query_result) == 0:
		response = {
			'isLoginSuccessful': 'false',
			'error': 'Invalid username provided'
		}
	else:
		if password == record[1]:
			response = {
				'isLoginSuccessful': 'true',
				'error': ''
			}
		else:
			response =  {
				'isLoginSuccessful': 'false',
				'error': 'Invalid password provided'
			}
	print(response)
	return response

