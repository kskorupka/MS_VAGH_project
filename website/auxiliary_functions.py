def contains_a_number(s):
    return any(i.isdigit() for i in s)


def get_bikes(items, locations):
    bikes = list(dict())
    bike_count = 1
    for item in items:
        for location in locations:
            if item.locationID == location.locationID:
                if item.type == 'Rower':
                    bikes.append({'itemID': (bike_count, item.itemID), 'location': {'name': location.name}})
                    bike_count += 1
                break
    return bikes


def get_scooters(items, locations):
    scooters = list(dict())
    scooter_count = 1
    for item in items:
        for location in locations:
            if item.locationID == location.locationID:
                if item.type == 'Hulajnoga':
                    scooters.append({'itemID': (scooter_count, item.itemID), 'location': {'name': location.name}})
                    scooter_count += 1
                break
    return scooters


def get_skateboards(items, locations):
    skateboards = list(dict())
    skateboard_count = 1
    for item in items:
        for location in locations:
            if item.locationID == location.locationID:
                if item.type == 'Deskorolka':
                    skateboards.append({'itemID': (skateboard_count, item.itemID), 'location': {'name': location.name}})
                    skateboard_count += 1
                break
    return skateboards
