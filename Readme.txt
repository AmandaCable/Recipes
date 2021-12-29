Flask Way to Run Server

Setup command
python -m pipenv install cryptography flask flask-bcrypt pymysql

Run command
python -m pipenv run flask run

Explanation
Flask finds the module through the environment variable 'FLASK_APP', which is setup in the '.env' file





Old Way to Run Server through 'server.py'

Setup command
python -m pipenv install cryptography flask flask-bcrypt pymysql

Run command
python -m pipenv run python server.py