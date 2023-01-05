from unittest import TestCase, mock
from events_manager import GenericEventsManager
from events_manager.exceptions import ObjectDoesExists


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
        self.assertEqual(type(obj), GenericEventsManager.EventObject)
    
    def test_get_exception(self):
        self.assertRaises(
            ObjectDoesExists,
            self.events_manager.get,
            'XP'
        )
    
    def test_update(self):
        self.events_manager._observers_obj_update_event = mock.MagicMock()
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
        self.assertTrue(self.events_manager._observers_obj_update_event.called)
    
    def test_delete(self):
        self.events_manager._observers_obj_delete_event = mock.MagicMock()
        data = {
            'state' : 'ON',
            'key' : 'XPTO'
        }
        new_obj = self.events_manager.get_factory_object(data)
        self.events_manager.create(new_obj)
        self.events_manager.delete(new_obj)
        self.assertFalse(self.events_manager.exists('XPTO'))
        self.assertTrue(self.events_manager._observers_obj_delete_event.called)
    
    def test_event_update_called_methods(self):
        self.events_manager.update = mock.MagicMock()
        data = {
            'state' : 'OFF',
            'key' : 'XPTO1'
        }
        self.events_manager.event_update(data)
        self.assertFalse(self.events_manager.update.called)
        self.events_manager.event_update(data)
        self.assertTrue(self.events_manager.update.called)