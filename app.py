from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/faq')
def hello_world():
    return render_template('index.html')


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
