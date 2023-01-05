from unittest import TestCase
from events_manager import GenericEventsManager, GenericObject


class GenericEventsManagerTestCase(TestCase):

    def setUp(self) -> None:
        self.events_manager = GenericEventsManager()
        return super().setUp()
    
    def test_attr_objects_dict(self):
        self.assertDictEqual(self.events_manager._objects_dict, {})
    
    def test_get_factory_object(self):
        data = {
            'state' : 'ON',
            'key' : 'XPTO'
        }
        new_obj = self.events_manager.get_factory_object(data)
        self.assertEqual(new_obj.key, 'XPTO')
        self.assertEqual(new_obj.state, 'ON')
        self.assertEqual(new_obj.get_key(), 'XPTO')
    
    def test_create(self):
        data = {
            'state' : 'ON',
            'key' : 'XPTO'
        }
        new_obj = self.events_manager.get_factory_object(data)
        self.assertFalse(self.events_manager.exists(new_obj.get_key()))
        self.events_manager.create(new_obj)
        self.assertTrue(self.events_manager.exists(new_obj.get_key()))
    
    def test_get(self):
        data = {
            'state' : 'ON',
            'key' : 'XPTO'
        }
        new_obj = self.events_manager.get_factory_object(data)
        self.events_manager.create(new_obj)
        obj = self.events_manager.get('XPTO')
        self.assertEqual(type(obj), GenericObject)
    
    def test_update(self):
        data = {
            'state' : 'ON',
            'key' : 'XPTO'
        }
        new_obj = self.events_manager.get_factory_object(data)
        self.events_manager.create(new_obj)
        data = {
            'state' : 'OFF',
            'key' : 'XPTO'
        }
        new_obj = self.events_manager.get_factory_object(data)
        self.events_manager.update(new_obj)
        obj = self.events_manager.get('XPTO')
        self.assertEqual(obj.state, 'OFF')
    
    def test_delete(self):
        data = {
            'state' : 'ON',
            'key' : 'XPTO'
        }
        new_obj = self.events_manager.get_factory_object(data)
        self.events_manager.create(new_obj)
        self.events_manager.delete(new_obj)
        self.assertFalse(self.events_manager.exists('XPTO'))