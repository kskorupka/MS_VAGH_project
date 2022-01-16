from unittest import TestCase
from ..auxiliary_functions import get_bikes, get_scooters, get_skateboards, check_if_item_is_available
from sqlalchemy import engine


class testForUser(TestCase):

    def testContains_a_number(self):
        pass

    def testGetBikes(self):
        from ..models import Location, Item

        # items = [engine.Row(1, 1, 'Rower', 'niebieski'), engine.Row(2, 2, 'Hulajnoga', 'niebieski'),
        #          engine.Row(3, 1, 'Deskorolka', 'niebieski'),
        #          engine.Row(4, 1, 'Rower', 'niebieski')]
        #
        # locations = [Location(1, 'Lok1', 'Lok1', 'Lo1'), Location(2, 'Lok2', 'Lok2', 'Lo2')]
        #
        # bikes = get_bikes(items, locations)
        #
        # correct_bikes = [[1, 1, "Rower", 20, "niebieski"], [4, 1, "Rower", 4, "niebieski"]]

        # self.assertEqual(bikes, correct_bikes)

    def testGet_skateboards(self):
        pass

    def testGet_scooters(self):
        pass

    def testIs_available(self):
        pass

    def testPerform_reservation(self):
        pass

    def testCheck_if_user_has_reservation(self):
        pass
