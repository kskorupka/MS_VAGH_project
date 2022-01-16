from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .auxiliary_functions import contains_a_number
from flask_login import login_user, login_required, logout_user, current_user

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
    from .auxiliary_functions import get_bikes, get_scooters, get_skateboards, perform_reservation

    reservations = Reservation.query.all()
    locations = Location.query.all()
    items = Item.query.all()
    bikes = get_bikes(items, locations, reservations)
    scooters = get_scooters(items, locations, reservations)
    skateboards = get_skateboards(items, locations, reservations)

    if request.method == 'POST':

        item_type = request.form.get('type')
        user_id = current_user.id
        reservations = Reservation.query.all()

        if item_type == 'Rower':
            item_id = request.form.get('bikes_available')
        elif item_type == 'Hulajnoga':
            item_id = request.form.get('scooters_available')
        else:
            item_id = request.form.get('skateboards_available')

        perform_reservation(user_id, reservations, item_id)
    return render_template("rent.html", user=current_user, bikes=bikes, scooters=scooters, skateboards=skateboards)


@auth.route('/return', methods=['GET', 'POST'])
@login_required
def return_item():
    from .auxiliary_functions import check_if_user_has_reservation, add_to_history
    from .models import Reservation, Location, Item

    user_id = current_user.id
    reservations = Reservation.query.all()
    locations = Location.query.all()

    if not check_if_user_has_reservation(user_id, reservations):
        flash('Nie wypożyczyłeś żadnego sprzętu.')
        return render_template("home.html", user=current_user)

    else:
        if request.method == 'POST':
            reservation = Reservation.query.filter_by(userID=user_id).first()
            location_id = request.form.get('locations')
            item = Item.query.filter_by(itemID=reservation.itemID).first()

            add_to_history(reservation, location_id)

            item.locationID = location_id
            db.session.commit()

            Reservation.query.filter_by(userID=user_id).delete()
            db.session.commit()

            flash('Zwrócono sprzęt')
            return render_template('home.html', user=current_user)
        return render_template("return.html", user=current_user, locations=locations)


@auth.route('/report', methods=['GET', 'POST'])
@login_required
def report():
    if request.method == 'POST':
        report = request.form.get('report')

        flash('Dziękujemy za zgłodzenie problemu')
    return render_template('report.html', user=current_user)


@auth.route('/announcement')
@login_required
def announcement():
    from .models import Announcement
    announcements = Announcement.query.order_by(Announcement.announcementID.desc()).all()
    return render_template("announcements.html", user=current_user, announcements=announcements)