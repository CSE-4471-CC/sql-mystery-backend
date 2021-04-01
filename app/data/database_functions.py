import csv

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


# path of USER_INFO table csv data
userinfo_data_path = DB_TABLE_DICT['USER_INFO']
# SQL query to insert records into user info table
userinfo_insert_query = 'INSERT into USER_INFO (User_ID, First_name, Last_name, Superhero_Name, Allergens) VALUES (? , ? , ? , ? , ?)'
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
purchaseorders_insert_query = 'INSERT into PURCHASE_ORDERS (PO_NUMBER, USER_ID, ITEM, COST, DATE_RECIEVED, TIME_RECIEVED) VALUES (? , ? , ? , ? , ? , ?)'
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
buildingaccess_insert_query = 'INSERT into BUILDING_ACCESS (Building_ID, Building_date, Building_time, User_ID) VALUES (? , ? , ? , ? )'
# read in csv data
with open(buildingaccess_data_path, newline='\n') as csvfile:
	buildingaccess_data = csv.reader(csvfile, delimiter=',')
	# skip header row
	next(buildingaccess_data, None)
	# insert records into database
	for record in buildingaccess_data:
		database.execute(buildingaccess_insert_query, record)
		database.commit()
			
			
