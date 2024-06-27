import time

from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, make_response
from flask_login import LoginManager, login_user, current_user, logout_user, UserMixin, login_required
import requests
from flask_sqlalchemy import SQLAlchemy
from requests import exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from requests.auth import HTTPBasicAuth

from PIL import Image

from bs4 import BeautifulSoup

import UserLogin
from models import User
import logging

app = Flask(__name__)



app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:0909@localhost:5432/test'
app.config["TEMPLATES_AUTO_RELOAD"] = True
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)

MAX_CONTENT_LENGTH = 1024 * 1024


ip_wemos = 'http://172.20.10.10'

# настройка login
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = ''

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True,nullable=False)
    password = db.Column(db.String(500), nullable=False)
    ip_address = db.Column(db.String(80), nullable=True)
    back_image = db.Column(db.LargeBinary(80), default=None)


    def __repr__(self):
        return f"<users {self.id}>"

def get_my_ip():
    return request.remote_addr


# Создание админа
@app.before_request
def create_adm():
    db.create_all()
    user = User.query.filter_by(username='admin').first()
    if not user:
        hashed_password = generate_password_hash('33886985')
        print(get_my_ip())
        admin = User(username='admin',password=hashed_password)   #сделать хэш пароля
        db.session.add(admin)
        db.session.commit()


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    response.headers['Expires'] = '0'
    response.headers['Pragma'] = 'no-cache'
    return response


########## ЛОГГИРОВАНИЕ #############
logger = logging.getLogger('app')
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('app.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
############################################


@login_manager.user_loader
def load_user(user_id):
    print('load_user')
    return User.query.get(int(user_id))


def get_users_from_db():
    return User.query.all()


def parse_status():
    auth = HTTPBasicAuth('admin', '0909')
    resp = requests.get(ip_wemos, auth=auth)
    soup = BeautifulSoup(resp.text, 'lxml')
    print(soup.encode('utf-8'))
    divs = soup.find_all('div')

    stat_list = []
    for div in divs:
        if div.get('class') == ['status']:
            for p in div.find_all('p'):
                for b in p.find_all('b'):
                    stat_list.append(b.text.strip())
            print(stat_list)
    return stat_list


@app.route('/',methods=['GET','POST'])
@login_required
def index():  # put application's code here
    if request.method == 'POST':
        auth = HTTPBasicAuth('admin', '0909')
        try:
            if request.form['submit_button'] == 'UP':
                try:
                    response = requests.get(ip_wemos+'/UP', auth=auth, timeout=5)
                    if response.status_code == 200:
                        stat_list = parse_status()
                        return render_template('index.html', username=current_user.username, status=stat_list)
                    else:
                        print('not auth')
                except exceptions.ConnectionError:
                    flash('Connection error', 'error')

            elif request.form['submit_button'] == 'DOWN':
                try:
                    response = requests.get(ip_wemos+'/DOWN', auth=auth, timeout=5)
                    if response.status_code == 200:
                        stat_list = parse_status()
                        return render_template('index.html', username=current_user.username, status=stat_list)
                    else:
                        print('not auth')
                except exceptions.ConnectionError:
                    flash('Connection error', 'error')


            elif request.form['submit_button'] == 'LEFT':
                try:
                    response = requests.get(ip_wemos+'/LEFT', auth=auth, timeout=5)
                    if response.status_code == 200:
                        stat_list = parse_status()
                        return render_template('index.html', username=current_user.username, status=stat_list)
                    else:
                        print('not auth')
                except exceptions.ConnectionError:
                    flash('Connection error', 'error')

            elif request.form['submit_button'] == 'RIGHT':
                try:
                    response = requests.get(ip_wemos+'/RIGHT', auth=auth, timeout=5)
                    if response.status_code == 200:
                        stat_list = parse_status()
                        return render_template('index.html', username=current_user.username, status=stat_list)
                    else:
                        print('not auth')
                except exceptions.ConnectionError:
                    flash('Connection error', 'error')

            elif request.form['submit_button'] == 'INVERSE':
                try:
                    response = requests.get(ip_wemos+'/INVERSE', auth=auth, timeout=5)
                    if response.status_code == 200:
                        stat_list = parse_status()
                        return render_template('index.html', username=current_user.username, status=stat_list)
                    else:
                        print('not auth')
                except exceptions.ConnectionError:
                    flash('Connection error', 'error')
            elif request.form['submit_button'] == 'ALL ON':
                try:
                    response = requests.get(ip_wemos+'/SwitchOn', auth=auth, timeout=5)
                    if response.status_code == 200:
                        stat_list = parse_status()
                        return render_template('index.html', username=current_user.username, status=stat_list)
                    else:
                        print('not auth')
                except exceptions.ConnectionError:
                    flash('Connection error', 'error')

            elif request.form['submit_button'] == 'ALL OFF':
                try:
                    response = requests.get(ip_wemos+'/SwitchOff', auth=auth,timeout=5)
                    if response.status_code == 200:
                        stat_list = parse_status()
                        return render_template('index.html', username=current_user.username, status=stat_list)
                    else:
                        print('not auth')
                except exceptions.ConnectionError:
                    flash('Connection error','error')


        except Exception as e:
            print(e)

    try:
        response = requests.get(ip_wemos+'/',timeout=3)
        print(response.status_code)
        stat_list = parse_status()
    except  exceptions.ConnectionError:
        print('not connect')
        stat_list = ['Not connected', 'Not connected', 'Not connected', 'Not connected']
    return render_template('index.html',username=current_user.username, status=stat_list)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index', username=current_user.username))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        # if username == 'admin' and password == 'admin':
        # user = User.query.filter_by(name=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            logger.info(f'Вход в аккаунт:{current_user.username}')
            try:
                ip_addr = get_my_ip()
                user.ip_address = ip_addr
                db.session.commit()
            except Exception as e:
                print(e)

            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logger.info(f'Выход из аккаунта:{current_user.username}')
    logout_user()
    flash('Вы вышли из аккаунта', "success")
    return redirect(url_for('login'))

# ?


@app.route('/profile/<username>', methods=['GET', 'POST'])
@login_required
def profile(username):
    if request.method == 'POST':
        if request.form['submit_button'] == 'Изменить':
            username = request.form['username_change']
            if username != current_user.username:
                flash('Invalid username', 'error')
                return redirect(url_for('profile', username=username))

            old_password = request.form['old_password']
            new_password = request.form['new_password']
            new_password_confirm = request.form['new_password2']
            user = User.query.filter_by(username=username).first()

            current_password = User.query.filter_by(username=user.username).first().password
            if check_password_hash(current_password, old_password):
                if new_password == new_password_confirm:
                    new_pass_user = User.query.filter_by(username=username).first()
                    new_pass_user.password = generate_password_hash(new_password)
                    db.session.commit()
                    flash('Пароль успешно изменён', 'success')
                    logger.info(f'Изменение пароля:{username}')
                else:
                    flash('Passwords do not match', 'error')

            else:
                flash('Invalid old password', 'error')




    if current_user.is_authenticated:
        if current_user.username == 'admin':
            return redirect(url_for('admin_panel'))


    return render_template("profile.html", username=current_user.username)



@app.route('/delete/<username>', methods=['GET', 'POST'])
@login_required
def delete(username):
    if current_user.username != 'admin':
        return redirect(url_for('index'))
    try:
        if username == 'admin':
            flash('Ошибка удаления', 'error')
            return redirect(url_for('profile', username=username))
        User.query.filter_by(username=username).delete()
        db.session.commit()
        flash(f'Пользователь {username} успешно удалён','success')
        logger.info(f'Удаление пользователя:{username}')
        return redirect(url_for('profile', username=username))
    except Exception:
        print("Something went wrong")
        flash('Ошибка удаления','error')


@app.route('/admin_panel', methods=['GET', 'POST'])
@login_required
def admin_panel():
    if current_user.username != 'admin':
        return redirect(url_for('index'))
    if request.method == 'POST':
        if request.form['submit_button'] == 'Изменить':
            username = request.form['username_change']
            #usernames_list = [user.username for user in User.query.all()]

            #if username not in usernames_list:
            if username != current_user.username:
                flash('Invalid username', 'error')
                return redirect(url_for('profile', username=current_user.username))
            old_password = request.form['old_password']
            new_password = request.form['new_password']
            new_password_confirm = request.form['new_password2']
            user = User.query.filter_by(username=username).first()

            current_password = User.query.filter_by(username=user.username).first().password
            if check_password_hash(current_password,old_password):
                if new_password == new_password_confirm:
                    new_pass_user = User.query.filter_by(username=username).first()
                    new_pass_user.password = generate_password_hash(new_password)
                    db.session.commit()
                    flash('Пароль успешно изменён','success')
                    logger.info(f'Изменение пароля:{current_user.username}')
                else:
                    flash('Passwords do not match', 'error')

            else:
                flash('Invalid old password', 'error')

#добавление пользователя
        elif request.form['submit_button'] == 'Добавить':
            try:
                username = request.form['new_user_name']
                u = User.query.filter_by(username=username).first()
                if u:
                    flash('Пользователь с таким именем уже существует',"error")
                    return redirect(url_for('profile', username=username))

                hash_pass = generate_password_hash(request.form['new_user_password'])
                user = User(username=request.form['new_user_name'],password=hash_pass)
                db.session.add(user)
                db.session.commit()
                flash('Пользователь добавлен успешно', category='success')
                logger.info(f'Добавление пользователя:{username}')
            except Exception as e:
                print(e)
                db.session.rollback()
                print('Ошибка добавления в БД!!!!')
                flash('Ошибка добавление пользователя', category='error')

    with open('app.log', 'r') as log_file:
        log_entries = log_file.readlines()
        print(log_entries)
    return render_template('admin.html', username=current_user.username,users=User.query.all(),log_entries=log_entries)


# @app.route('/user_avatar')
# @login_required
# def user_avatar():
#     img = current_user.back_image
#
#     if img is None:
#         return '#adffff'
#     if not img:
#         return ""
#
#     h = make_response(img)
#     h.headers['Content-Type'] = 'image/jpg'
#     print(h)
#
#     return h
#
#
# @app.route('/upload', methods=['GET', 'POST'])
# @login_required
# def upload():
#     if request.method == 'POST':
#         file = request.files['file']
#         if file and UserLogin.verifyExt(file.filename):
#             try:
#                 img = file.read()
#                 current_user.back_image = img
#                 db.session.commit()
#                 flash('Аватар обновлён','success')
#             except FileNotFoundError as e:
#                 flash('Ошибка чтения файла','error')
#         else:
#             flash('Ошибка обновления аватара','error')
#     return redirect(url_for('profile',username=current_user.username))
#
#
# def parse():
#     resp = requests.get('http://192.168.0.112')




if __name__ == '__main__':
    app.run(host="192.168.0.109", port=5000, debug=True,ssl_context=('/certs/mk_cert.pem', '/certs/mk_key.pem'))


# --host 0.0.0.0 --port 5000 --cert=cert.pem --key=key.pem