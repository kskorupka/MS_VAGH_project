def contains_a_number(s):
    return any(i.isdigit() for i in s)


def get_bikes(items, locations, reservations):
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
    for reservation in reservations:
        if reservation.userID == user_id:
            return True
    return False


def perform_reservation(user_id, reservations, item_id, ):
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
    for reservation in reservations:
        if reservation.itemID == item_id:
            return False
    return True


def add_to_history(reservation, location_id):
    from .models import History, db
    from datetime import datetime as date

    histories = History.query.all()
    new_history = History(historyID=len(histories) + 1, userID=reservation.userID, locationID=location_id,
                          itemID=reservation.itemID, fromDate=reservation.fromDate, toDate=date.now())
    db.session.add(new_history)
    db.session.commit
