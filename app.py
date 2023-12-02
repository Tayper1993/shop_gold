from datetime import timedelta

from flask import Flask, jsonify, render_template, request
from flask_jwt_extended import create_refresh_token, JWTManager
from sqlalchemy.exc import IntegrityError

from config import Config
from oits.models import News, session, Users

app = Flask(__name__)
app.config.from_object(Config)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)

client = app.test_client()

jwt = JWTManager(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/signin', methods=['GET'])
def signin():
    return render_template('sign_in.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
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
    else:
        return render_template('register.html')


@app.route('/login', methods=['POST'])
def login():
    params = request.json
    user = Users.authenticate(**params)
    access_token = user.get_token()
    refresh_token = create_refresh_token(user.id)
    return jsonify(
        {
            'access_token': access_token,
            'refresh_token': refresh_token,
        }
    )


@app.route('/news', methods=['POST'])
def create_news():
    data = request.get_json()
    title = data['title']
    content = data['content']
    author_id = data['author_id']

    news = News(title=title, content=content, author_id=author_id)
    session.add(news)
    session.commit()
    return jsonify({'successfully': 'Новость успешно создана!'}), 200


@app.route('/news', methods=['GET'])
def get_news():
    news = session.query(News).all()

    news_list = []
    for n in news:
        news_list.append(
            {
                'id': n.id,
                'title': n.title,
                'content': n.content,
                'author_id': n.author_id,
            }
        )

    return render_template('news.html', news_list=news_list)


@app.route('/news/<int:news_id>', methods=['DELETE'])
def delete_news(news_id):
    news = session.query(News).filter_by(id=news_id).first()
    if news:
        session.delete(news)
        session.commit()
        return ({'successfully': 'Новость успешно удалена'}), 200
    else:
        return ({'successfully': 'Новость не найдена'}), 200


@app.route('/news/<int:news_id>', methods=['PUT'])
def edit_news(news_id):
    news = session.query(News).filter_by(id=news_id).first()
    if news:
        data = request.get_json()
        title = data['title']
        content = data['content']
        edit_news = News(title=title, content=content)
        session.commit()
        return ({'successfully': 'Новость успешно отредактирована'}), 200
    else:
        return ({'successfully': 'Новость не найдена'}), 200


if __name__ == '__main__':
    app.run(debug=True)
