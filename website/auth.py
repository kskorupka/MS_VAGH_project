from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    :return: html template of login
    This function moves current_user to login's part. User may log in only if he has an account.
    """
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
    """
    :return: html template of login
    This function moves current_user to login's part. After logging out User is not able to perform app's actions
    (renting items).
    """
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    """
    :return: html template of sign_up
    This function moves current_user to sign_up's part. User may sign up only if his email doesn't exist in DataBase.
    """
    from .auxiliary_functions import check_if_data_is_correct

    if request.method == 'POST':

        '''get all user's information'''
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        second_name = request.form.get('secondName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        phone = request.form.get('phoneNumber')

        '''check if user exists in DataBase or given data is incorrect'''
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Konto już istnieje.', category='error')
        elif check_if_data_is_correct(email, first_name, second_name, password1, password2, phone):

            '''add user to DataBase'''
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
    """
    :return: html template of rent
    This function moves current_user to rent's part. User may rent an item only if he doesn't have any reservations.
    """
    from .models import Item, Location, Reservation
    from .auxiliary_functions import get_bikes, get_scooters, get_skateboards, perform_reservation, get_rows

    '''get all important lists so User may access current data'''
    reservations = get_rows(Reservation)
    locations = get_rows(Location)
    items = get_rows(Item)
    bikes = get_bikes(items, locations, reservations)
    scooters = get_scooters(items, locations, reservations)
    skateboards = get_skateboards(items, locations, reservations)

    '''perform user's action'''
    if request.method == 'POST':

        item_type = request.form.get('type')
        user_id = current_user.id

        if item_type == 'Rower':
            item_id = request.form.get('bikes_available')
        elif item_type == 'Hulajnoga':
            item_id = request.form.get('scooters_available')
        else:
            item_id = request.form.get('skateboards_available')

        '''create new reservation'''
        perform_reservation(user_id, reservations, item_id)
        return render_template("home.html", user=current_user)
    return render_template("rent.html", user=current_user, bikes=bikes, scooters=scooters, skateboards=skateboards)


@auth.route('/return', methods=['GET', 'POST'])
@login_required
def return_item():
    """
    :return: html template of return
    This function moves current_user to return's part. User may return an item only if he has a reservation.
    """
    from .auxiliary_functions import check_if_user_has_reservation, add_to_history, get_rows
    from .models import Reservation, Location, Item

    '''get all important lists so User may access current data'''
    user_id = current_user.id
    reservations = get_rows(Reservation)
    locations = get_rows(Location)

    '''check if user may return anything'''
    if not check_if_user_has_reservation(user_id, reservations):
        flash('Nie wypożyczyłeś żadnego sprzętu.')
        return render_template("home.html", user=current_user)
    else:
        '''if so, perform his action'''
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
    """
    :return: html template of report
    This function moves current_user to report's part.
    """
    from .auxiliary_functions import add_report
    if request.method == 'POST':

        '''create new report'''
        new_report = request.form.get('report')
        if len(new_report) == 0:
            flash('Nie możesz wysłać pustego zgłoszenia')
        else:
            add_report(user_id=current_user.id, description=new_report)
            flash('Dziękujemy za zgłodzenie problemu')
            return render_template("home.html", user=current_user)
    return render_template('report.html', user=current_user)


@auth.route('/announcement')
@login_required
def announcement():
    """
    :return: html template of announcement
    This function moves current_user to announcement's part
    """
    from .models import Announcement

    '''get all announcements and show them to user'''
    announcements = Announcement.query.order_by(Announcement.announcementID.desc()).all()
    return render_template("announcements.html", user=current_user, announcements=announcements)
