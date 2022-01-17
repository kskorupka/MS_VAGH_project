def contains_a_number(s):
    """
    :param s: text to check
    :return: True, if text contains any numbers
    """
    return any(i.isdigit() for i in s)


def contains_a_character(s):
    import re
    """
    :param s: text to check
    :return: True, if text contains any characters
    """
    for i in s:
        if re.match('[A-Za-z]', i):
            return True
    return False


def get_bikes(items, locations, reservations):
    """
    :param items: all items in DataBase
    :param locations: all locations in DataBase
    :param reservations: current reservations in DataBase
    :return: list of bike's dictionaries: (bike_count, item.itemID) : location.name
    """
    bikes = list(dict())
    bike_count = 1
    for location in locations:
        for item in items:
            if item.locationID == location.locationID and check_if_item_is_available(item.itemID, reservations):
                if item.type == 'Rower':
                    bikes.append({'itemID': (bike_count, item.itemID), 'location': {'name': location.name}})
                    bike_count += 1
    return bikes


def get_scooters(items, locations, reservations):
    """
    :param items: all items in DataBase
    :param locations: all locations in DataBase
    :param reservations: current reservations in DataBase
    :return: list of scooter's dictionaries: (bike_count, item.itemID) : location.name
    """
    scooters = list(dict())
    scooter_count = 1
    for location in locations:
        for item in items:
            if item.locationID == location.locationID and check_if_item_is_available(item.itemID, reservations):
                if item.type == 'Hulajnoga':
                    scooters.append({'itemID': (scooter_count, item.itemID), 'location': {'name': location.name}})
                    scooter_count += 1
    return scooters


def get_skateboards(items, locations, reservations):
    """
    :param items: all items in DataBase
    :param locations: all locations in DataBase
    :param reservations: current reservations in DataBase
    :return: list of scooter's dictionaries: (bike_count, item.itemID) : location.name
    """
    skateboards = list(dict())
    skateboard_count = 1
    for location in locations:
        for item in items:
            if item.locationID == location.locationID and check_if_item_is_available(item.itemID, reservations):
                if item.type == 'Deskorolka':
                    skateboards.append(
                        {'itemID': (skateboard_count, item.itemID), 'location': {'name': location.name}})
                    skateboard_count += 1
    return skateboards


def check_if_user_has_reservation(user_id, reservations):
    """
    :param user_id: current_user's id in DataBase
    :param reservations: current reservations in DataBase
    :return: True, if user have any reservation
    """
    for reservation in reservations:
        if reservation.userID == user_id:
            return True
    return False


def perform_reservation(user_id, reservations, item_id, ):
    """
    :param user_id: current_user's id in DataBase
    :param reservations: current reservations in DataBase
    :param item_id: item's ID in DataBase which current_user wants to rent
    This function adds a new record in Reservation's Table and informs user about it
    """
    from flask import flash
    from .models import Reservation, db
    from datetime import datetime as date
    if check_if_user_has_reservation(user_id, reservations):
        flash('Już masz wypożyczony sprzęt. Aby wypożyczyć następny, zwróć obecnie posiadany sprzęt.')
    else:
        new_reservation = Reservation(reservationID=len(reservations) + 1, userID=user_id, itemID=item_id,
                                      fromDate=date.now())
        db.session.add(new_reservation)
        db.session.commit()
        flash('Wypożyczono sprzęt')


def check_if_item_is_available(item_id, reservations):
    """
    :param item_id: item's ID in DataBase which current_user wants to rent
    :param reservations: current reservations in DataBase
    :return: False, if any user rented this item
    """
    for reservation in reservations:
        if reservation.itemID == item_id:
            return False
    return True


def add_to_history(reservation, location_id):
    """
    :param reservation: current reservations in DataBase
    :param location_id: location's ID in DataBase that current_user chose to leave the item at
    This function adds a new record in History's Table
    """
    from .models import History, db
    from datetime import datetime as date

    histories = History.query.all()
    new_history = History(historyID=len(histories) + 1, userID=reservation.userID, locationID=location_id,
                          itemID=reservation.itemID, fromDate=reservation.fromDate, toDate=date.now())
    db.session.add(new_history)
    db.session.commit()


def add_report(user_id, description):
    """
    :param user_id: current_user's id in DataBase
    :param description: report that user has just written
    """
    from .models import Report, db

    reports = Report.query.all()
    new_report = Report(reportID=len(reports) + 1, userID=user_id, description=str(description))

    for report in reports:
        print(type(report))
    db.session.add(new_report)
    db.session.commit()


def get_rows(table):
    """
    :param table: table to get data from
    :return: list of rows from table
    """
    return table.query.all()


def check_if_data_is_correct(email, first_name, second_name, password1, password2, phone):
    """
    :param email: user's email
    :param first_name: user's name
    :param second_name: user's surname
    :param password1: user's password
    :param password2: user's password (to check)
    :param phone: user's phone number
    :return: True, if all data meets the requirements
    """
    from flask import flash

    if len(email) < 4 or email.find("@") == -1:
        flash('Niepoprawny email', category='error')
        return False
    elif len(first_name) < 3 or len(second_name) < 3:
        flash('Imię oraz nazwisko powinno być dłuższe niż 1 litera', category='error')
        return False
    elif contains_a_number(first_name) == True or contains_a_number(second_name) == True:
        flash('Imię oraz nazwisko nie powinno zawierać liczb', category='error')
        return False
    elif password1 != password2:
        flash('Hasła nie są takie same', category='error')
        return False
    elif len(password1) < 8 or contains_a_number(password1) == False:
        flash('Hasło powinno składać się z 8 znaków oraz zawierać co najmniej jedną liczbę', category='error')
        return False
    elif len(phone) != 9 or contains_a_character(phone):
        flash('Numer telefonu powinien składać się z 9 cyfr', category='error')
        return False
    return True
