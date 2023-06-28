from flask import Flask, render_template
from flask_jwt_extended import JWTManager
from sqlalchemy.orm import declarative_base


app = Flask(__name__)

Base = declarative_base()


jwt = JWTManager(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


# @app.route('/contacts')   TODO Сделать страницу с контактами
# def hello_world():
#     return render_template('index.html')
#
#
# @app.route('/accounts/login') TODO Сделать страницу с регистрацией
# def hello_world():
#     return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
