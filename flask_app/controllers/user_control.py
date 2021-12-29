from flask import render_template, redirect, session, request
from flask_app.models.user_model import User
from flask_app import app, bcrypt

@app.route('/')
def index():
    return render_template('reg_login.html')

@app.route('/dashboard')
def dashboard():
    if 'id' not in session:
        return redirect('/')
    user = User.retrieve_one_user(id=session['id'])
    return render_template('dashboard.html', user=user)

#ACTIONS
@app.route('/register', methods=['POST'])
def register():
    if not User.validate_reg(request.form):
        return redirect('/')
    user_data = {
        **request.form,
        'password' : bcrypt.generate_password_hash(request.form['password'])
    }
    session['id'] = User.create(user_data)
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    if not User.validate_login(request.form):
        return redirect('/')
    user = User.retrieve_one_user(email=request.form['login_email'])
    session['id']= user.id
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')



