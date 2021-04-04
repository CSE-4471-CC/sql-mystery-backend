# written by Lia Ferguson
import os
import platform
import pprint
import json

USERS_COLUMNS = ['User_ID', 'Password']
USER_INFO_COLUMNS = ['User_ID', 'First_name', 'Last_name', 'Superhero_Name']
QUESTIONNAIRE_COLUMNS = ['User_ID', 'Favorite_food', 'Favorite_hobby', 'Favorite_drink', 'Allergies']
PURCHASE_ORDERS_COLUMNS = ['PO_NUMBER', 'USER_ID', 'ITEM,COST', 'DATE_RECIEVED', 'TIME_RECIEVED']
BUILDING_ACCESS_COLUMNS = ['Building_ID', 'Building_date', 'Building_time', 'User_ID']
CORRECT_RESULTS = {
	'S4_B1': [(12592,)],
	'S4_B2': [(12592, 'steak', 'stand-up comedy', 'coffee', 'almonds')],
	'S5_B1': [(15687, 'almonds'), (17896, 'almonds')],
	'S5_S': ['Natasha Romanoff', 'Bruce Banner']
}


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
	return columns

def format_query_results(query_results, table_columns):
	formatted_results = []
	matches_correct_results = False
	records = [tuple(y for y in row) for row in query_results]
	print(records)
	for record in records:
		format_record = {}
		i = 0
		for item in record:
			format_record[table_columns[i]] = item
			i += 1
		formatted_results.append(format_record)
			
	return formatted_results

def check_expected_results(query_results, game_step):
	matches_correct_results = False
	correct_results = CORRECT_RESULTS[game_step]
	correct_results_length = len(correct_results)
	comparison = [] # index corresponds to record number, 1 = same, 0 = different
	records = [tuple(y for y in row) for row in query_results]
	if len(records) == correct_results_length:
		for i in range (0, correct_results_length):
			for record in records:
				sum_match = 0
				for element in correct_results[i]:
					if element in record:
						sum_match += 1				
				if sum_match == len(record):
					comparison.append(1)
				else: 
					comparison.append(0)
		sum_comparison = 0
		for num in comparison:
			sum_comparison += num
		if sum_comparison == len(correct_results):
			matches_correct_results = True
	return matches_correct_results

def print_results_to_file(formatted_results, game_step):
	path = os.path.expanduser("~")
	rest_of_path = ''
	if(platform.system() == 'Windows'):
		rest_of_path = '\Desktop\SQL-Mystery-Game-Files'
	else:
		rest_of_path = '/Desktop/Sql-Mystery-Game-Files/'
	path += rest_of_path
	if not os.path.isdir(path):
		os.mkdir(path)
	f = open(path + 'Clues.txt', 'a')
	if game_step == 'S4_B1':
		f.write("STEP 4 CLUES\n")
		f.write("Tony Stark's User ID\n\n")
	elif game_step == 'S4_B2':
		f.write("Tony Stark's Questionnaire Data\n\n")
	elif game_step == 'S5_B1':
		f.write("STEP 5 CLUES\n")
		f.write("Discover Possible Almond Snackers\n\n")
	elif game_step == 'S5_S':
		f.write("Suspects\n\n")
	f.write(json.dumps(formatted_results, indent=4, sort_keys=False))
	f.write('\n\n')
	f.close()

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

def check_suspect(name, game_step):
	correct = False
	suspects = CORRECT_RESULTS[game_step]
	for suspect in suspects:
		if name.casefold() == suspect.casefold():
			correct = True
			break
	return correct
	