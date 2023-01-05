from unittest import TestCase
from events_manager import GenericEventsManager, GenericObserver
from events_manager.exceptions import InvalidObserver


class GenericEventsManagerTestCase(TestCase):

    def setUp(self) -> None:
        self.events_manager = GenericEventsManager()
        return super().setUp()
    
    def test_validate_observer(self):
        data = {
            'state' : 'ON',
            'key' : 'XPTO'
        }
        new_obj = self.events_manager.get_factory_object(data)
        observer = 'teste'
        self.assertRaises(
            InvalidObserver,
            new_obj.validate_observer,
            observer
        )
        observer = GenericObserver()
        self.assertTrue(new_obj.validate_observer(observer))
    
    def test_obj_subscribe_unsubscribe(self):
        data = {
            'state' : 'ON',
            'key' : 'XPTO'
        }
        new_obj = self.events_manager.get_factory_object(data)
        observer = GenericObserver()
        self.assertEqual(len(new_obj.observers), 0)
        new_obj.subscribe(observer)
        self.assertEqual(len(new_obj.observers), 1)
        new_obj.unsubscribe(observer)
        self.assertEqual(len(new_obj.observers), 0)
    
    
