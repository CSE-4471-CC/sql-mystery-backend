""" code written by Lia Ferguson:
		all code besides the code written by Andrew Fecher
"""
"""code written by Andrew Fecher:
		line 18, lines 106-117
"""
# Edited By Andrew Fecher
import os
import platform
import pprint
import json

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
	clues = ''
	if platform.system() == 'Windows':
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
	