from unittest import TestCase
from events_manager import GenericEventsManager


class GenericEventsManagerAllTestCase(TestCase):

    def setUp(self) -> None:
        self.events_manager = GenericEventsManager()
        return super().setUp()
       
    
    def test_all_method(self):
        data = {
            'state' : 'OFF',
            'key' : 'XPTO1'
        }
        self.events_manager.event_update(data)
        data = {
            'state' : 'ON',
            'key' : 'XPTO2'
        }
        self.events_manager.event_update(data)
        self.assertEqual(len(self.events_manager.all()), 2)