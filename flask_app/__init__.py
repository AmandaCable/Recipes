from flask_bcrypt import Bcrypt
from flask import Flask

app = Flask(__name__)
app.secret_key= 'pspsps'
bcrypt = Bcrypt(app)

DB = 'recipes'
