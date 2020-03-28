from flask import Flask
from flask import render_template, redirect, request
from data import db_session
from data.users import User
from data.jobs import Jobs
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


db_session.global_init('db/data.sqlite')
session = db_session.create_session()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
