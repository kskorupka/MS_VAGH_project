from flask import Blueprint, render_template, request, flash, redirect, url_for
from website.auxiliary_functions import contains_a_number
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Zalogowano pomyślnie!', category='success')
            else:
                flash('Hasło niepoprawne, spróbuj ponownie', category='error')
        else:
            flash('Takie konto nie istnieje', category='error')
    return render_template("login.html", bool=True)


@auth.route('/logout')
def logout():
    return "<p>Logout</p>"


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        secondName = request.form.get('secondName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Konto już istnieje', category='error')
        elif len(email) < 4 or email.find("@") == -1:
            flash('Niepoprawny email', category='error')
        elif len(firstName) < 3 or len(secondName) < 3:
            flash('Imię oraz nazwisko powinno być dłuższe niż 1 litera', category='error')
        elif contains_a_number(firstName) == True or contains_a_number(secondName) == True:
            flash('Imię oraz nazwisko nie powinno zawierać liczb', category='error')
        elif password1 != password2:
            flash('Hasła nie są takie same', category='error')
        elif len(password1) < 8 or contains_a_number(password1) == False:
            flash('Hasło powinno składać się z 8 znaków oraz zawierać co najmniej jedną liczbę', category='error')
        else:
            # add user to a database
            new_user = User(email=email, name=firstName, surname=secondName, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Konto zostało utworzone poprawnie', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html")
