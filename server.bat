@ECHO OFF

:SETUP
ECHO. & ECHO. & ECHO --SETUP--
python -m pipenv install cryptography flask flask-bcrypt pymysql

:SERVE
ECHO. & ECHO. & ECHO --SERVE--
REM python -m pipenv run flask run
python -m pipenv run python server.py

ECHO. & ECHO.
SET /P input="Press enter to restart server. (Enter 'n' to exit.) "
IF "%input%" NEQ "n" GOTO:SERVE

PAUSE