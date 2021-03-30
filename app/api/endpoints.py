from flask import Flask, Blueprint, request, jsonify;
from app.db get db

# lines 5-33 written by Lia Ferguson
bp = Blueprint('endpoints', __name__, url_prefix='/endpoints')

NUM_RECORDS_USERS_TABLE = 5 # replace this number with actual number of records in database

# endpoint for Step 1 SQL Injection Task 
@bp.route('/login_query', methods = ['POST'])
def login_query():
  database = get_db()

  user_id = request.get_json()['user_id']
  password = request.get_json()['password']
  # wrong way to compose SQL query based on secure coding practices
  # this allows for SQL Injection to occur
  login_q = 'SELECT * WHERE User_ID = {u_id} AND Password = {pwd}'.format(u_id = user_id, pwd = password)
   
  query_result = db.execute(login_q).fetchall()
  response = {}
  if len(query_result) == NUM_RECORDS_USER_TABLE:
    response = {
      'status': 'SUCCESS'
      'message': 'Congratulations! You successfully used SQL Injection to bypass authentication.'
    }
  else:
    response = {
      'status': 'ERROR'
      'message': 'SQL Injection was not successful, please try again.'
    }

  return jsonify(response)
  


