from flask import Flask
from data import db_session
from data.users import User
from data.jobs import Jobs

app = Flask(__name__)
app.config['SECRET_KEY'] = 'MarsIT1535'


@app.route('/')
@app.route('/index')
def index():
    return 'Test page'


db_session.global_init('db/data.sqlite')
session = db_session.create_session()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
