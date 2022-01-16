from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .auxiliary_functions import contains_a_number
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime as date

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
        first_name = request.form.get('firstName')
        second_name = request.form.get('secondName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        phone = request.form.get('phoneNumber')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Konto już istnieje.', category='error')
        elif len(email) < 4 or email.find("@") == -1:
            flash('Niepoprawny email', category='error')
        elif len(first_name) < 3 or len(second_name) < 3:
            flash('Imię oraz nazwisko powinno być dłuższe niż 1 litera', category='error')
        elif contains_a_number(first_name) == True or contains_a_number(second_name) == True:
            flash('Imię oraz nazwisko nie powinno zawierać liczb', category='error')
        elif password1 != password2:
            flash('Hasła nie są takie same', category='error')
        elif len(password1) < 8 or contains_a_number(password1) == False:
            flash('Hasło powinno składać się z 8 znaków oraz zawierać co najmniej jedną liczbę', category='error')
        else:
            # add user to a database
            new_user = User(email=email, password=generate_password_hash(password1, method='sha256'), name=first_name,
                            surname=second_name, phone=phone)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Konto zostało utworzone pomyślnie!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)


@auth.route('/rent', methods=['GET', 'POST'])
@login_required
def rent():
    from .models import Item, Location, Reservation
    from .auxiliary_functions import get_bikes, get_scooters, get_skateboards

    locations = Location.query.all()
    items = Item.query.all()

    bikes = get_bikes(items, locations)
    scooters = get_scooters(items, locations)
    skateboards = get_skateboards(items, locations)

    if request.method == 'POST':

        item_type = request.form.get('type')
        user_id = current_user.id

        if item_type == 'Rower':
            item_id = request.form.get('bikes_available')
        elif item_type == 'Hulajnoga':
            item_id = request.form.get('scooters_available')
        else:
            item_id = request.form.get('skateboards_available')

        reservations = Reservation.query.all()
        new_reservation = Reservation(reservationID=len(reservations), userID=user_id, itemID=item_id,
                                      fromDate=date.now(), toDate=date.now())
        db.session.add(new_reservation)
        db.session.commit()
        flash('Wypożyczono sprzęt')
    return render_template("rent.html", user=current_user, bikes=bikes, scooters=scooters, skateboards=skateboards)


@auth.route('/return', methods=['GET', 'POST'])
@login_required
def return_item():
    # TODO delete reservation
    # https://www.youtube.com/watch?v=1nxzOrLWiic&ab_channel=TechWithTim
    # 1)  Go
    # to
    # user.html and add
    # the
    # below
    # code:
    # < form
    # action = "{{ url_for('delete') }}" >
    #          < input
    # type = "submit"
    # value = "Delete my record" >
    #         < / form >
    #
    #             2)  Add
    # the
    # below
    # snippet
    # for delete module in your flask file:
    #     @
    #     app.route("/delete")
    #
    # def delete():
    #     if "user" in session and "email" in session:
    #         user = session["user"]
    #         email = session["email"]
    #         users.query.filter_by(name=user).delete()
    #         users.query.filter_by(email=email).delete()
    #         db.session.commit()
    #         flash("Record deleted successfully!")
    #     elif "user" in session and "email" not in session:
    #         user = session["user"]
    #         if not users.query.filter_by(name=user).first():
    #             flash("Unable to delete since there is no record found!")
    #         else:
    #             users.query.filter_by(name=user).delete()
    #             db.session.commit()
    #             flash("Record deleted successfully!")
    #     else:
    #         flash("Unable to delete record!")
    #     return redirect(url_for("user"))
    return render_template("return.html", user=current_user)
