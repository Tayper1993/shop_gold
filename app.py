from flask import Flask, render_template, request
from flask_jwt_extended import JWTManager
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

from config import Config
from models import Users


app = Flask(__name__)
app.config.from_object(Config)


client = app.test_client()

Base = declarative_base()

engine = create_engine('postgresql+psycopg2://scot:tiger@localhost:5432/mydatabase')

session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


jwt = JWTManager(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/register', methods=['POST'])
def register():
    params = request.json
    user = Users(**params)
    session.add(user)
    session.commit()
    token = user.get_token()
    return {'access_token': token}


@app.route('/login', methods=['POST'])
def login():
    params = request.json
    user = Users.authenticate(**params)
    token = user.get_token()
    return {'access_token': token}


if __name__ == '__main__':
    app.run(debug=True)
