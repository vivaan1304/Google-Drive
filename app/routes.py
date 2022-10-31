from flask_login.utils import login_required, logout_user
from werkzeug.utils import redirect, send_from_directory
from werkzeug.wrappers import response
from app import app, db
from flask import render_template, url_for, redirect, flash, request,  send_file, send_from_directory, safe_join, abort, Response
from app.forms import LoginForm, RegisterForm, UploadForm
from flask_login import logout_user, current_user, login_user, login_required
from app.models import User
import os
# import urllib.parse


@app.route('/')
@app.route('/index')
@login_required
def index():
    form = UploadForm()
    lst = os.listdir(os.path.join(app.config['UPLOAD_LOCATION'], os.path.join(current_user.username, 'root')))
    print(lst)
    return render_template('index.html', title='home', form = form, lst = lst, os = os, app=app, cur_path = [])
# TODO : Secure_filename function
@app.route('/upload', methods=['POST'])
@login_required
def upload():
    for up_file in request.files.getlist('file'):
        if up_file.filename != '':
            up_file.save(os.path.join(app.config['UPLOAD_LOCATION'], current_user.username, up_file.filename))
    flash('your files have been saved')
    return redirect(url_for('index'))



@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form  = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid Username or Password.')
            return redirect(url_for('index'))
        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html', title = 'Login', form=form)

@app.route('/download/<fname>', methods=['GET', 'POST'])
@login_required
def download(fname):

    lol = os.path.join(app.config['UPLOAD_LOCATION'], current_user.username)
    return send_from_directory(directory=lol, path=fname,  as_attachment=True)
    


@login_required
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['POST', 'GET'])
def register():
    form  = RegisterForm()
    if form.validate_on_submit():
        u = User()
        u.username = form.username.data
        u.email = form.email.data
        u.set_password(form.password.data)
        db.session.add(u)
        db.session.commit()
        os.makedirs(os.path.join(app.config['UPLOAD_LOCATION'], u.username, 'root'), exist_ok=True)
        flash('Congratulations you are now a registered user.')
        return redirect(url_for('login'))
    return render_template('register.html', form = form, title='Register')

@login_required
@app.route('/createfolder', methods=['POST'])
def create_folder():
    name = request.json["new_folder"] 
    path = request.json["path"] + [name] # array consisting of all folders
    path[0] = 'root'
    print('/'.join(path))
    path_final = '/'.join(path)
    os.makedirs(os.path.join(app.config['UPLOAD_LOCATION'], current_user.username,path_final), exist_ok=True)
    
    return name