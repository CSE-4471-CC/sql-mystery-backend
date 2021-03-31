# sql-mystery-backend

This repository houses all of the backend API and database that will provide additional functionality to our SQL Murder Mystery game.

## How to get started
1. Clone the repository to local machine
2. Create a python virtual environment by running the following command: `python3 -m venv env`
3. Activate virtual environment by running the following command: 
   1.For Mac: `source env/bin/activate`
   2.For Windows: `source env/Scripts/activate`
5. Install dependencies by running the following command: `python3 -m pip install -r requirements.txt`
6. Set flask environment variable by running the following command: `export FLASK_APP=app`
7. Check to make sure that your current directory is "sql-mystery-backend", the following command won't work if you are in another directory
8. Instantiate database by running the following command: `flask init-db` 
   1. The database file will show up in a folder called "instance" and it will be named "game_db.sqlite"
9. When you need to start the backend server, do so by running the following command: `flask run`



**Important note: you will have to repeat steps 3-7 every time you start working on the project again after closing it out**
