
USERS_COLUMNS = ['User_ID', 'Password']
USER_INFO_COLUMNS = ['User_ID', 'First_name', 'Last_name', 'Superhero_Name']
QUESTIONNAIRE_COLUMNS = ['User_ID', 'Favorite_food', 'Favorite_hobby', 'Favorite_drink', 'Allergies']
PURCHASE_ORDERS_COLUMNS = ['PO_NUMBER', 'USER_ID', 'ITEM,COST', 'DATE_RECIEVED', 'TIME_RECIEVED']
BUILDING_ACCESS_COLUMNS = ['Building_ID', 'Building_date', 'Building_time', 'User_ID']

CORRECT_RESULTS = {
	'S4_B1': [(12592,)],
	'S4_B2': [(12592, 'steak', 'stand-up comedy', 'coffee', 'almonds')],
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