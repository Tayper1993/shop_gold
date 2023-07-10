from datetime import timedelta

from flask import Flask, render_template, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_refresh_token
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError

from config import Config
from models import session, Users

app = Flask(__name__)
app.config.from_object(Config)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

client = app.test_client()

engine = create_engine('postgresql+psycopg2://scot:tiger@localhost:5432/mydatabase')

jwt = JWTManager(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
@jwt_required()
def about():
    return render_template('about.html')


@app.route('/register', methods=['POST'])
def register():
    params = request.json
    user = Users(**params)

    try:
        session.add(user)
        session.commit()
    except IntegrityError:
        session.rollback()
        return jsonify({'error': 'Ошибка регистрации пользователя'}), 400

    access_token = user.get_token()
    return jsonify({'access_token': access_token})


@app.route('/login', methods=['POST'])
def login():
    params = request.json
    user = Users.authenticate(**params)
    access_token = user.get_token()
    refresh_token = create_refresh_token(user.id)
    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
    })


if __name__ == '__main__':
    app.run(debug=True)
