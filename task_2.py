"""
Создать базу данных для хранения информации о книгах в библиотеке.
База данных должна содержать две таблицы: "Книги" и "Авторы".
В таблице "Книги" должны быть следующие поля: id, название, год издания,
количество экземпляров и id автора.
В таблице "Авторы" должны быть следующие поля: id, имя и фамилия.
Необходимо создать связь между таблицами "Книги" и "Авторы".
Написать функцию-обработчик, которая будет выводить список всех книг с
указанием их авторов.

"""

from flask import Flask, render_template
from model_3 import db, Book, Author
from random import randint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.cli.command('init-db')
def init_db():
    db.create_all()


@app.cli.command('fill-db')
def fill_db():
    for i in range(1, 6):
        new_author = Author(firstname=f'Имя{i}', lastname=f'Фамилия{i}')
        db.session.add(new_author)
    db.session.commit()

    for i in range(1, 11):
        for j in range(1, 6):
            new_book = Book(book_name=f'Название книги{i + randint(0, 100)}',
                            year_publishing=1900 + randint(0, 123),
                            number_copies=1000 + randint(0, 1000),
                            id_author=j)
            db.session.add(new_book)
    db.session.commit()


@app.route('/listbook/')
def list_book():
    books = Book.query.all()
    context = {'books': books}
    return render_template('listbook.html', **context)


if __name__ == '__main__':
    app.run()
