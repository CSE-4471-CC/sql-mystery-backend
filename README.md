# sql-mystery-backend

This repository houses all of the backend API and database that will provide additional functionality to our SQL Murder Mystery game.

## How to get started
1. Clone the repository to local machine
2. Create a python virtual environment by running the following command: `python3 -m venv env`
3. Activate virtual environment by running the following command: `source env/bin/activate`
4. Install dependencies by running the following command: `python3 -m pip install -r requirements.txt`
5. Set flask environment variable by running the following command: `export FLASK_APP=flask`
6. Instantiate database by running the following command: `flask init-db` 
   1. The database file will show up in a folder called "instance" and it will be named "game_db.sqlite"
7. When you need to start the backend server, do so by running the following command: `flask run`



**Important note: you will have to repeat steps 3-5 every time you start working on the project again after closing it out**
