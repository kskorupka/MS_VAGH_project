from flask import Blueprint, render_template, request, flash, redirect, url_for
from sqlalchemy import select
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .auxiliary_functions import contains_a_number
from flask_login import login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import functions


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
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Hasło niepoprawne, spróbuj ponownie.', category='error')
        else:
            flash('Takie konto nie istnieje.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        secondName = request.form.get('secondName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        phone = request.form.get('phoneNumber')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Konto już istnieje.', category='error')
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
            new_user = User(email=email, password=generate_password_hash(password1, method='sha256'), name=firstName, surname=secondName, phone=phone)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Konto zostało utworzone pomyślnie!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)


@auth.route('/rent', methods=['GET', 'POST'])
@login_required
def rent():
    from .models import Item, Location
    # bikes = select(functions.array_agg(Item.))
    # bikes = select(Item.type, Location.name).where(Item.type == "Rower")
    # bike_rows = Item.select().where(Item.type.__eq__('Rower'))
    bikes = list(dict())
    # bike_rows = db.execute(select(Item))
    # for itemID, locationID, type, weight, color in bike_rows:
    #     location = Location.select().where(Location.locationID.__eq__(locationID))
    #     bikes.append({'itemID': itemID, 'location' : {'name': location.name}})



    bikes.append({'itemID' : 1, 'location' : {'name': 'Kapitol'}})
    if request.method == 'POST':
        flash('Wypożyczono sprzęt')
    return render_template("rent.html", user=current_user, bikes=bikes)

