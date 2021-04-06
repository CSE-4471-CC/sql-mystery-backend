# from endpoints.py
""" endpoints written by Lia Ferguson:
		/login_bypass
		/login_query
		/trojan_horse
		/suspect
		/login

		with the exception of the two try - except blocks and json.dumps() lines written by Andrew Fecher
		in /login_query
"""
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
	
	login_q = 'SELECT * FROM USERS WHERE User_ID = {quote}{u_id} AND Password = {pwd}'.format(
							quote=quote, u_id = user_id, pwd = password)

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
	
	login_q = 'SELECT * FROM USERS WHERE User_ID = {quote}{u_id} AND Password = {quote}{pwd}'.format(
							quote=quote, u_id = user_id, pwd = password)

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
		formatted_query_results =''
		try:
			table_columns = queried_table_columns(commands[1])
			formatted_query_results = format_query_results(all_query_results[1], table_columns, game_step)
		except Exception as e:
			print(e)
			formatted_query_results = 'ERROR'
		match_expected_results = check_expected_results(all_query_results[1], game_step)
	if len(formatted_query_results) > 0:
		if match_expected_results:
			print_results_to_file(formatted_query_results, game_step)
			response = {
				'isQuerySuccessful': 'true',
				'correctResults': 'true',
				'results': json.dumps(formatted_query_results),
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
				'results': json.dumps(formatted_query_results),
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
	print(json.dumps(formatted_query_results))
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

# from database_functions.py
# lines 6-33 written by Lia Ferguson
# lines 49-91 written by Tom Chmura
# dictionary that maps table name to the path of the csv data to populate it
DB_TABLE_DICT = {
	'BUILDING_ACCESS': 'app/data/BUILDING_ACCESS.csv',
	'COMPUTER_ACCESS': 'app/data/COMPUTER_ACCESS.csv',
	'COMPUTER_TERMINALS': 'app/data/COMPUTER_TERMINALS.csv',
	'QUESTIONNAIRE': 'app/data/QUESTIONNAIRE.csv',
	'USER_INFO': 'app/data/USER_INFO.csv', 
	'USERS': 'app/data/USERS.csv',
	'PURCHASE_ORDERS': 'app/data/PURCHASE_ORDERS.csv'
}

# read in data for csv files, and format records properly for insertion into DB
# proper format needed = list of tuples with data in order by columns
# ex. for USERS table
#     return = [(1234, password), (2345, pwd123)]
def get_initial_data(database):
	# path of USERS table csv data
	users_data_path = DB_TABLE_DICT['USERS']
	# SQL query to insert records into users table
	users_insert_query = 'INSERT into USERS (User_ID, Password) VALUES (? , ?)'
	# read in csv data
	with open(users_data_path, newline='\n') as csvfile:
		user_data = csv.reader(csvfile, delimiter=',')
		# skip header row
		next(user_data, None)
		# insert records into database
		for record in user_data:
			database.execute(users_insert_query, record)
			database.commit()

	# path of QUESTIONNAIRE table csv data
	questionnaire_data_path = DB_TABLE_DICT['QUESTIONNAIRE']
	# SQL query to insert records into questionnaire table
	questionnaire_insert_query = 'INSERT into QUESTIONNAIRE (User_ID, Favorite_food, Favorite_hobby, Favorite_drink, Allergies) VALUES (? , ? , ? , ?, ?)'
	# read in csv data
	with open(questionnaire_data_path, newline='\n') as csvfile:
		questionnaire_data = csv.reader(csvfile, delimiter=',')
		# skip header row
		next(questionnaire_data, None)
		# insert records into database
		for record in questionnaire_data:
			database.execute(questionnaire_insert_query, record)
			database.commit()

	# path of USER_INFO table csv data
	userinfo_data_path = DB_TABLE_DICT['USER_INFO']
	# SQL query to insert records into user info table
	userinfo_insert_query = 'INSERT into USER_INFO (User_ID, First_name, Last_name, Superhero_Name) VALUES (? , ? , ? , ?)'
	# read in csv data
	with open(userinfo_data_path, newline='\n') as csvfile:
		userinfo_data = csv.reader(csvfile, delimiter=',')
		# skip header row
		next(userinfo_data, None)
		# insert records into database
		for record in userinfo_data:
			database.execute(userinfo_insert_query, record)
			database.commit()	


	# path of PURCHASE_ORDERS table csv data
	purchaseorders_data_path = DB_TABLE_DICT['PURCHASE_ORDERS']
	# SQL query to insert records into purchase orders table
	purchaseorders_insert_query = 'INSERT into PURCHASE_ORDERS (Po_number, User_ID, Item, Cost, Time_received) VALUES (? , ? , ? , ? , ?)'
	# read in csv data
	with open(purchaseorders_data_path, newline='\n') as csvfile:
		purchaseorders_data = csv.reader(csvfile, delimiter=',')
		# skip header row
		next(purchaseorders_data, None)
		# insert records into database
		for record in purchaseorders_data:
			database.execute(purchaseorders_insert_query, record)
			database.commit()
			

	# path of BUILDING_ACCESS table csv data
	buildingaccess_data_path = DB_TABLE_DICT['BUILDING_ACCESS']
	# SQL query to insert records into building access table
	buildingaccess_insert_query = 'INSERT into BUILDING_ACCESS (Building_ID, Building_time, User_ID) VALUES (? , ? , ? )'
	# read in csv data
	with open(buildingaccess_data_path, newline='\n') as csvfile:
		buildingaccess_data = csv.reader(csvfile, delimiter=',')
		# skip header row
		next(buildingaccess_data, None)
		# insert records into database
		for record in buildingaccess_data:
			database.execute(buildingaccess_insert_query, record)
			database.commit()
			
# from schema.sql
#Written by Tom Chmura
#small updates to USER_INFO, QUESTIONNAIRE, BUILDING_ACCESS, and PURCHASE_ORDERS tables by Lia Ferguson

-- Table: BUILDING_ACCESS
CREATE TABLE BUILDING_ACCESS(
Building_ID INT NOT NULL,
Building_time TIME NOT NULL,
User_ID INT NOT NULL,
FOREIGN KEY(User_ID) references USERS(User_ID));

-- Table: QUESTIONNAIRE
CREATE TABLE QUESTIONNAIRE(
User_ID INT NOT NULL,
Favorite_food VARCHAR(30),
Favorite_drink VARCHAR(30),
Favorite_hobby VARCHAR(30),
Allergies VARCHAR(30),
PRIMARY KEY(User_ID)
FOREIGN KEY(User_ID) references USERS(User_ID));

-- Table: USER_INFO
CREATE TABLE USER_INFO(
User_ID INT NOT NULL,
First_name VARCHAR(20) NOT NULL,
Last_name VARCHAR(20),
Superhero_Name VARCHAR(30),
PRIMARY KEY(User_ID)
FOREIGN KEY(User_ID) references USERS(User_ID));

-- Table: USERS
CREATE TABLE USERS(
User_ID INT NOT NULL,
Password VARCHAR(30) NOT NULL,
PRIMARY KEY(User_ID));

-- Table: PURCHASE_ORDERS
CREATE TABLE PURCHASE_ORDERS (
PO_NUMBER     INT          NOT NULL,
USER_ID       INT          NOT NULL,
ITEM          VARCHAR (30) NOT NULL,
COST          DOUBLE       NOT NULL,
TIME_RECEIVED TIME,
PRIMARY KEY (PO_NUMBER)
FOREIGN KEY(User_ID) references USERS(User_ID));

# from helper_functions.py
""" code written by Lia Ferguson:
		all code besides the code written by Andrew Fecher
"""
"""code written by Andrew Fecher:
		line 18, lines 106-117
"""

# Data structures to hold columns of data tab;es
USERS_COLUMNS = ['User_ID', 'Password']
USER_INFO_COLUMNS = ['User_ID', 'First_name', 'Last_name', 'Superhero_Name']
QUESTIONNAIRE_COLUMNS = ['User_ID', 'Favorite_food', 'Favorite_hobby', 'Favorite_drink', 'Allergies']
PURCHASE_ORDERS_COLUMNS = ['Po_number', 'User_ID', 'Item', 'Cost',  'Time_Received']
BUILDING_ACCESS_COLUMNS = ['Building_ID', 'Building_time', 'User_ID']
SQLITE_MASTER_COLUMNS = ['type', 'name', 'tabl_name', 'rootpage', 'sql']
#Data structure to hold expected SQL Results
CORRECT_RESULTS = {
	'S3_B1': [('BUILDING_ACCESS',), ('QUESTIONNAIRE',), ('USER_INFO',), ('USERS',), ('PURCHASE_ORDERS',)],
	'S4_B1': [(12592, 'Tony', 'Stark'),
						(15687, 'Natasha', 'Romanoff'),
						(15685, 'Scott', 'Lang'),
						(15972, 'Peter', 'Parker'),
						(15423, 'Steve', 'Rogers'),
						(15976, 'Thanos', ''),
						(17896, 'Bruce', 'Banner')],
	'S4_B2': [('steak', 'stand-up comedy', 'coffee', 'almonds')],
	'S5_B1': [(15687, 'almonds'), (17896, 'almonds')],
	'S5_S': ['Natasha Romanoff', 'Bruce Banner'],
	'S6_B1': [('Building_ID',), ('Building_time',), ('User_ID',)],
	'S6_B2': [(15687, '12:55 pm'), (17896, '12:40 pm')],
	'S6_B3': [(15972, '10:30 am'), (15976, '11:00 am')],
	'S6_S': ['Peter Parker', 'Thanos'],
	'S7_B1': [(156834, 15972, 'Coffee Creamer', 5.12, '5:00 pm'),
						(156853, 15976, 'Almond Coffee Creamer', 5.23, '5:00 pm'), 
						(438657, 15972, 'Popcorn', 10.25,'12:00pm')],
	'S7_S': ['Thanos'],
	'S7_B2': [(15976, 'IAmInevitable')]
}

# Parses out columns that are involved in the SQL Injection Query passed in by player
def queried_table_columns(query):
	columns = []
	columns_and_indices = {} # list that keeps track of column ordering in the query
	if query.casefold().find('questionnaire') != -1:
		if query.find('*') != -1:
			columns = QUESTIONNAIRE_COLUMNS
		else:
			for column in QUESTIONNAIRE_COLUMNS:
				query = query.casefold().partition('from')[0]
				if query.find(column.casefold()) != -1:
					columns_and_indices[query.find(column.casefold())] = column
			indices = list(columns_and_indices.keys())
			indices.sort()
			for index in indices:
				columns.append(columns_and_indices[index])
	elif query.casefold().find('user_info') != -1:
		if query.find('*') != -1:
			columns = USER_INFO_COLUMNS
		else:
			for column in USER_INFO_COLUMNS:
				query = query.casefold().partition('from')[0]
				if query.find(column.casefold()) != -1:
					columns_and_indices[query.find(column.casefold())] = column
			indices = list(columns_and_indices.keys())
			indices.sort()
			for index in indices:
				columns.append(columns_and_indices[index])
	elif query.casefold().find('users') != -1:
		if query.find('*') != -1:
			columns = USERS_COLUMNS
		else:
			for column in USERS_COLUMNS:
				query = query.casefold().partition('from')[0]
				if query.find(column.casefold()) != -1:
					columns_and_indices[query.find(column.casefold())] = column
			indices = list(columns_and_indices.keys())
			indices.sort()
			for index in indices:
				columns.append(columns_and_indices[index])
	elif query.casefold().find('purchase_orders') != -1:
		if query.find('*') != -1:
			columns = PURCHASE_ORDERS_COLUMNS
		else:
			for column in PURCHASE_ORDERS_COLUMNS:
				query = query.casefold().partition('from')[0]
				if query.find(column.casefold()) != -1:
					columns_and_indices[query.find(column.casefold())] = column
			indices = list(columns_and_indices.keys())
			indices.sort()
			for index in indices:
				columns.append(columns_and_indices[index])
	elif query.casefold().find('building_access') != -1:
		if query.find('*') != -1:
			columns = BUILDING_ACCESS_COLUMNS
		else:
			for column in BUILDING_ACCESS_COLUMNS:
				query = query.casefold().partition('from')[0]
				if query.find(column.casefold()) != -1:
					columns_and_indices[query.find(column.casefold())] = column
			indices = list(columns_and_indices.keys())
			indices.sort()
			for index in indices:
				columns.append(columns_and_indices[index])
	elif query.casefold().find('sqlite_master') != -1:
		if query.find('*') != -1:
			columns = SQLITE_MASTER_COLUMNS
		else:
			for column in SQLITE_MASTER_COLUMNS:
				query = query.casefold().partition('from')[0]
				if query.find(column.casefold()) != -1:
					columns_and_indices[query.find(column.casefold())] = column
			indices = list(columns_and_indices.keys())
			indices.sort()
			for index in indices:
				columns.append(columns_and_indices[index])

	return columns

# Formats query results nicely from sqlite3 data structures into dictionaries 
# for later JSON parsing
def format_query_results(query_results, table_columns, game_step):
	formatted_results = []
	records = [tuple(y for y in row) for row in query_results]
	print(records)
	if len(table_columns) == 0:
		for record in records:
			format_record = {}
			if game_step == 'S6_B1':
				format_record['Column'] = record[0]
			formatted_results.append(format_record)
	else:
		for record in records:
			format_record = {}
			i = 0
			for item in record:
				format_record[table_columns[i]] = item
				i += 1
			formatted_results.append(format_record)			
	return formatted_results

# check whether or not returned records from 
# SQL query match the expected output
def check_expected_results(query_results, game_step):
	matches_correct_results = False
	correct_results = CORRECT_RESULTS[game_step]
	correct_results_length = len(correct_results)
	comparison = [] # index corresponds to record number, 1 = same, 0 = different
	records = [tuple(y for y in row) for row in query_results]
	if len(records) == correct_results_length:
		for i in range(0, len(records)):
			sum_match = 0
			for j in range(0, len(records[0])):
				if correct_results[i][j] in records[i]:
					sum_match += 1 
			if sum_match == len(records[i]):
				comparison.append(1)
			else:
				comparison.append(0)
		print(comparison)
		sum_comparison = 0
		for num in comparison:
			sum_comparison += num
		print(sum_comparison)
		if sum_comparison == len(correct_results):
			matches_correct_results = True
	return matches_correct_results

# Print results of SQL Injection to Clues.txt file to 
# assist player with game play
def print_results_to_file(formatted_results, game_step):
	path = os.path.expanduser("~")
	rest_of_path = ''
		if platform.system() == 'Windows' :
		rest_of_path = '\Desktop\SQL-Mystery-Game-Files'
		clues='\Clues.txt'
	else:
		rest_of_path = '/Desktop/Sql-Mystery-Game-Files/'
		clues='Clues.txt'
	path += rest_of_path
	if not os.path.isdir(path):
		os.mkdir(path)
	f = open(path + clues, 'a')
	if game_step == 'S4_B1':
		f.write("STEP 4 CLUES\n")
		f.write("Employee User ID\'s\n\n")
	elif game_step == 'S4_B2':
		f.write("Tony Stark's Questionnaire Data\n\n")
	elif game_step == 'S5_B1':
		f.write("STEP 5 CLUES\n")
		f.write("Discover Possible Almond Snackers\n\n")
	elif game_step == 'S5_S':
		f.write("Suspect\n\n")
	f.write(json.dumps(formatted_results, indent=4, sort_keys=False))
	f.write('\n\n')
	f.close()

# execute "trojan horse" - download
# confession file onto player's computer with their name filled in
def execute_trojan_horse(first_name, last_name):
	path = os.path.expanduser("~")
	rest_of_path = ''
	if(platform.system() == 'Windows'):
		rest_of_path = '\Desktop\SQL-Mystery-Game-Files\Confidential'
		file_path = '\For Police.txt'
	else:
		rest_of_path = '/Desktop/Sql-Mystery-Game-Files/Confidential'
		file_path = '/For Police.txt'
	path += rest_of_path

	os.mkdir(path)
	f_read = open('app/data/trojan_horse_confess_template.txt', 'r')
	f_write = open(path + file_path, 'a')
	f_write.write(f_read.read())
	f_write.write(first_name + " " + last_name)

	f_read.close()
	f_write.close()

# verify if the suspect entered by player is correct
def check_suspect(name, game_step):
	correct = False
	suspects = CORRECT_RESULTS[game_step]
	for suspect in suspects:
		if name.casefold() == suspect.casefold():
			correct = True
			break
	return correct
	