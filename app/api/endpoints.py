from flask import Flask, Blueprint, request, jsonify;
from app.db import get_db

# lines 5-33 written by Lia Ferguson
# Edited and supplemeneted by Andrew Fecher
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

	commands = login_q.split(";", -1)
	query_results = list()
	error = ''
	try:
		for command in commands:
			query_results.append(database.execute(command).fetchall())
	except Exception as e:
		query_results.clear()
		error = e.args
	
	contents = ''
	i = 0;
	if len(query_results) == len(commands):
		for table in query_results:
			contents += 'Query #' + str(i) + ' Results\n'
			i += 1
			for row in table:
				for element in row:
					contents += str(element).replace('\n','/n').replace('\t','/t').replace('\r','/r') + 'tt\t'
				contents += '\n'
			contents += '\n\n'
	else:
		contents = error

	query_result = '';
	if len(query_results) > 0:
		query_result = query_results[0]
	if len(query_result) > 0:
		response = {
			'isQuerySuccessful': 'true',
			'status': 'SUCCESS',
			'results': contents,
			'login': query_result[0][0],
			'message': 'Congratulations! You successfully used SQL Injection to bypass authentication.'
		}

	else:
		response = {
			'isQuerySuccessful': 'false',
			'status': 'ERROR',
			'results': contents,
			'login': 'ERROR',
			'message': 'SQL Injection was not successful, please try again.'
		}
	print(contents)
	print(response)
	print(user_id)
	return jsonify(response)

