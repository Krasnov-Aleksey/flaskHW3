"""
Создайте форму регистрации пользователя с использованием Flask-WTF. Форма должна
содержать следующие поля:
○ Имя пользователя (обязательное поле)
○ Электронная почта (обязательное поле, с валидацией на корректность ввода email)
○ Пароль (обязательное поле, с валидацией на минимальную длину пароля)
○ Подтверждение пароля (обязательное поле, с валидацией на совпадение с паролем)
После отправки формы данные должны сохраняться в базе данных (можно использовать SQLite)
и выводиться сообщение об успешной регистрации. Если какое-то из обязательных полей не
заполнено или данные не прошли валидацию, то должно выводиться соответствующее
сообщение об ошибке.
Дополнительно: добавьте проверку на уникальность имени пользователя и электронной почты в
базе данных. Если такой пользователь уже зарегистрирован, то должно выводиться сообщение
об ошибке.
"""

from flask import Flask, render_template, request
from flask_wtf import CSRFProtect
from form_1 import RegisterForm
from model_4 import db, Users

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'
csrf = CSRFProtect(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase1.db'
db.init_app(app)


@app.cli.command('init-db')
def init_db():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        user = Users.query.all()
        for item in user:
            if item.username == username and item.email == email:
                return 'Пользователь существует'
        new_user = Users(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return 'Регистрация прошла успешно'
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run()
