from unittest import TestCase
from ..auxiliary_functions import contains_a_number, get_bikes, get_scooters, get_skateboards, \
    check_if_item_is_available, check_if_user_has_reservation, contains_a_character
from ..models import Item, Location, Reservation, User
from datetime import datetime as date


class Test(TestCase):
    '''
       A class used to test functions

       Methods
       ----------
        testContains_a_number(self)
            Tests function contains_a_number from auxiliary_functions

        testGetBikes(self)
            Tests function get_bikes from auxiliary_functions

        testGet_skateboards(self)
            Tests function get_skateboards from auxiliary_functions

        testGet_scooters(self)
            Tests function get_scooters from auxiliary_functions

        testIs_available(self)
            Tests function check_if_item_is_available from auxiliary_functions

        testCheck_if_user_has_reservation(self)
            Tests check_if_user_has_reservation from auxiliary_functions

        testContains_character(self)
            Tests contains_a_character from auxiliary_functions
       '''

    def testContains_a_number(self):
        text1 = "alamakota"
        self.assertEquals(False, contains_a_number(text1))

        text2 = "ipsa123"
        self.assertEquals(True, contains_a_number(text2))

    def testGetBikes(self):
        items = [Item(itemID=1, locationID=1, type='Rower', color='niebieski'),
                 Item(itemID=2, locationID=1, type='Hulajnoga', color='niebieski'),
                 Item(itemID=3, locationID=2, type='Deskorolka', color='niebieski'),
                 Item(itemID=4, locationID=2, type='Rower', color='niebieski')]

        correct_bikes = list(dict())
        correct_bikes.append({'itemID': (1, 1), 'location': {'name': 'Lok1'}})
        correct_bikes.append({'itemID': (2, 4), 'location': {'name': 'Lok2'}})

        locations = [Location(locationID=1, description='Lok1', nearTo='Lok1', name='Lok1'),
                     Location(locationID=2, description='Lok2', nearTo='Lok2', name='Lok2')]

        reservations = []

        bikes = get_bikes(items, locations, reservations)

        self.assertEquals(correct_bikes, bikes)

    def testGet_skateboards(self):
        items = [Item(itemID=1, locationID=1, type='Deskorolka', color='niebieski'),
                 Item(itemID=2, locationID=1, type='Hulajnoga', color='niebieski'),
                 Item(itemID=3, locationID=2, type='Deskorolka', color='niebieski'),
                 Item(itemID=4, locationID=2, type='Rower', color='niebieski')]

        correct_skateboards = list(dict())
        correct_skateboards.append({'itemID': (1, 1), 'location': {'name': 'Lok1'}})
        correct_skateboards.append({'itemID': (2, 3), 'location': {'name': 'Lok2'}})

        locations = [Location(locationID=1, description='Lok1', nearTo='Lok1', name='Lok1'),
                     Location(locationID=2, description='Lok2', nearTo='Lok2', name='Lok2')]

        reservations = []

        skateboards = get_skateboards(items, locations, reservations)

        self.assertEquals(correct_skateboards, skateboards)

    def testGet_scooters(self):
        items = [Item(itemID=1, locationID=1, type='Hulajnoga', color='niebieski'),
                 Item(itemID=2, locationID=1, type='Hulajnoga', color='niebieski'),
                 Item(itemID=3, locationID=2, type='Deskorolka', color='niebieski'),
                 Item(itemID=4, locationID=2, type='Rower', color='niebieski')]

        correct_scooters = list(dict())
        correct_scooters.append({'itemID': (1, 1), 'location': {'name': 'Lok1'}})
        correct_scooters.append({'itemID': (2, 2), 'location': {'name': 'Lok1'}})

        locations = [Location(locationID=1, description='Lok1', nearTo='Lok1', name='Lok1'),
                     Location(locationID=2, description='Lok2', nearTo='Lok2', name='Lok2')]

        reservations = []

        scooters = get_scooters(items, locations, reservations)

        self.assertEquals(correct_scooters, scooters)

    def testIs_available(self):
        item1 = Item(itemID=1, locationID=1, type='Hulajnoga', color='niebieski')
        item2 = Item(itemID=2, locationID=1, type='Hulajnoga', color='niebieski')
        reservations = [Reservation(reservationID=1, userID=1, itemID=1, fromDate=date.now()),
                        Reservation(reservationID=2, userID=2, itemID=3, fromDate=date.now())]

        self.assertEquals(False, check_if_item_is_available(item1.itemID, reservations))
        self.assertEquals(True, check_if_item_is_available(item2.itemID, reservations))

    def testCheck_if_user_has_reservation(self):
        reservations = [Reservation(reservationID=1, userID=1, itemID=1, fromDate=date.now()),
                        Reservation(reservationID=2, userID=2, itemID=3, fromDate=date.now())]
        user1 = User(id=1, email='test@gmail.com', password='', name='test', surname='test', phone='123456789')
        user2 = User(id=3, email='test@gmail.com', password='', name='test', surname='test', phone='123456789')

        self.assertEquals(True, check_if_user_has_reservation(user1.id, reservations))
        self.assertEquals(False, check_if_user_has_reservation(user2.id, reservations))

    def testContains_character(self):
        text1 = "1234"
        text2 = "123asda5"
        text3 = "23A1n"

        self.assertEquals(False, contains_a_character(text1))
        self.assertEquals(True, contains_a_character(text2))
        self.assertEquals(True, contains_a_character(text3))
