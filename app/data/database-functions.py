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
def get_initial_data(table_name):
