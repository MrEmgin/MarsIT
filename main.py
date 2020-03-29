from flask import Flask
from flask import render_template, redirect, request
from data import db_session
from data.users import User
from data.jobs import Jobs
from random import randint
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'MarsIT1535'


@app.route('/')
@app.route('/index')
def index():
    return 'Test page'


@app.route('/works')
def works():
    works = session.query(Jobs).all()
    params = {'title': 'Works log',
              'session': session,
              'works': works,
              'User': User
              }
    return render_template('works_log.html', **params)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register_form.html', title='Register form', warning='')
    elif request.method == 'POST':
        user = User()
        user.surname = request.form['surname']
        user.name = request.form['name']
        user.age = int(request.form['age'])
        user.position = request.form['position']
        user.speciality = request.form['speciality']
        user.address = request.form['address']
        user.email = request.form['email']
        user.set_password(request.form['password'])
        if user.hashed_password != request.form['repeat']:
            return render_template('register_form.html', title='Register form', warning='Passwords are different!')

        session.add(user)
        session.commit()
        return 'Sent<br>' + str(user)


db_session.global_init('db/data.sqlite')
session = db_session.create_session()

if __name__ == '__main__':
    for user in session.query(User).all():
        user.set_password(user.hashed_password)
    session.commit()
    quit()
    app.run(host='127.0.0.1', port=8080)
