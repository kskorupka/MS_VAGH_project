from unittest import TestCase
from ..auxiliary_functions import get_bikes, get_scooters, get_skateboards

class testForUser(TestCase):

    def testGetBikes(self):
        from ..models import Location, Item
        # items = list([1, 1, "Rower", 20, "niebieski"], [2, 2, "Hulajnoga", 4, "niebieski"],
        #              [3, 1, 'Deskorolka', 4, "niebieski"], [4, 1, "Rower", 4, "niebieski"])
        #
        # locations = list([1, "Lok1", "Lok1", "Lo1"],[1, "Lok2", "Lok2", "Lo2"])
        #
        # bikes = get_bikes(items,locations)


