from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

engine = create_engine("postgresql+psycopg2://scot:tiger@localhost:5432/mydatabase")
Base.metadata.create_all(engine)

Session = sessionmaker(autoflush=False, bind=engine)


app = Flask(__name__)


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
    app.run(
        debug=True
    )
