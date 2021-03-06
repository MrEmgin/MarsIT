from flask import Flask
from flask import render_template, redirect, request, make_response, abort
from flask import session as sess

from flask_login import LoginManager
from flask_login import login_user, logout_user, current_user, login_required

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField, DateField
from wtforms.validators import DataRequired, Email

import datetime

from data import db_session
from data.users import User
from data.jobs import Jobs


class LoginForm(FlaskForm):
    email = StringField('Email: ', validators=[DataRequired(), Email()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in')


class AddWorkForm(FlaskForm):
    team_leader = IntegerField("Enter team leader's id", validators=[DataRequired()])
    job = StringField('Job title: ', validators=[DataRequired()])
    work_size = IntegerField('Work size in hours: ', validators=[DataRequired()])
    collaborators = StringField('Collaborators list (enter ids with " ," between')
    end_date = StringField('Enter the deadline date "%Y-%m-%d %H:%M:%S"')
    is_finished = BooleanField("Is the job finished?")
    submit = SubmitField("Add")


app = Flask(__name__)
app.config['SECRET_KEY'] = 'MarsIT1535'


@app.route('/')
@app.route('/index')
def index():
    return render_template('base.html', title='Start page')


@app.route('/works')
@login_required
def works():
    session = db_session.create_session()
    works = session.query(Jobs).all()
    params = {'title': 'Works log',
              'session': session,
              'works': works,
              'User': User,
              'deleted': False,
              'warnings': []
              }
    return render_template('works_log.html', **params)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register_form.html', title='Register form', warning='')
    elif request.method == 'POST':
        session = db_session.create_session()

        user = User()
        user.surname = request.form['surname']
        user.name = request.form['name']
        user.age = int(request.form['age'])
        user.position = request.form['position']
        user.speciality = request.form['speciality']
        user.address = request.form['address']
        user.email = request.form['email']
        user.set_password(request.form['password'])
        if request.form['password'] != request.form['repeat']:
            return render_template('register_form.html', title='Register form', warning='Passwords are different!')

        session.add(user)
        session.commit()
        return 'Sent<br>' + str(user)


@app.route('/test')
def test():
    visits_count = int(request.cookies.get('visits_count', 0))
    if visits_count:
        res = make_response(f"You've visited this page for {visits_count} times!")
        res.set_cookie('visits_count', str(visits_count + 1), max_age=60 * 60 * 24 * 365 * 2)
    else:
        res = make_response('You are visiting this page for the first time')
        res.set_cookie('visits_count', '1', max_age=60 * 60 * 24 * 365 * 2)
    return res


@app.route('/session_test')
def session_test():
    # session.pop('visits_count', None)
    if 'visits_count' in sess:
        sess['visits_count'] = sess.get('visits_count') + 1
    else:
        sess['visits_count'] = 1
    return render_template('base.html', title='Sessions')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        return render_template('login.html', message='Invalid login or password', form=form)
    return render_template('login.html', form=form)


@app.route('/add_work', methods=['GET', 'POST'])
@login_required
def add_work():
    form = AddWorkForm()
    if request.method == 'POST':
        session = db_session.create_session()

        data = form.end_date.data
        date = datetime.datetime.strptime(data, "%Y-%m-%d %H:%M:%S")

        job = Jobs()
        job.team_leader = form.team_leader.data
        job.job = form.job.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.end_date = date
        job.is_finished = form.is_finished.data

        session.add(job)
        session.commit()
        return redirect('/works', code=302)

    return render_template('add_work.html', title='Adding work', form=form, warnings=[], data=[''] * 6)


@app.route('/edit_work/<int:id>', methods=['POST', 'GET'])
@login_required
def edit_work(id):
    form = AddWorkForm()
    session = db_session.create_session()
    warnings = []
    data = []
    job = session.query(Jobs).filter(Jobs.id == id).first()

    if request.method == 'GET':
        if not job:
            warnings.append(':( Job is not found :( (404)')
        else:
            data = [job.job, job.team_leader, job.work_size, job.collaborators, job.end_date, job.is_finished]
            if job.author != current_user.id and current_user.id != 1:
                warnings.append('Access denied.')
                data = [''] * 6
        return render_template('add_work.html', title='Edit work', form=form, warnings=warnings, data=data)
    elif request.method == 'POST':
        data = form.end_date.data
        date = datetime.datetime.strptime(data, "%Y-%m-%d %H:%M:%S")

        job.team_leader = form.team_leader.data
        job.job = form.job.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.end_date = date
        job.is_finished = form.is_finished.data

        session.commit()
        return redirect('/works', code=302)
    return render_template('base.html', title='test')


@app.route('/delete_work/<int:id>')
@login_required
def delete_work(id):
    global warnings
    session = db_session.create_session()
    job = session.query(Jobs).filter(Jobs.id == id).first()
    if not job:
        return redirect('/works', code=302)
    if current_user.id != 1 and current_user.id != job.author:
        warnings.append("You don't have enough rights to delete this")
        return redirect('/works', code=302)
    session.delete(job)
    session.commit()

    return redirect('/works', code=302)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


login_manager = LoginManager()
login_manager.init_app(app)

db_session.global_init('db/data.sqlite')

warnings = []


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
