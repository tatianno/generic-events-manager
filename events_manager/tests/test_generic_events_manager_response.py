from unittest import TestCase
from events_manager import GenericEventsManager


class GenericEventsManagerResponseTestCase(TestCase):

    def setUp(self) -> None:
        self.events_manager = GenericEventsManager()
        return super().setUp()

    def test_event_update_response(self):
        data = {
            'state' : 'OFF',
            'key' : 'XPTO1'
        }
        response = self.events_manager.event_update(data)
        self.assertEqual(type(response), GenericEventsManager.EventResponse)
        self.assertEqual(type(response.event_obj), GenericEventsManager.EventObject)
        self.assertTrue(response.created)
        response = self.events_manager.event_update(data)
        self.assertEqual(type(response), GenericEventsManager.EventResponse)
        self.assertEqual(type(response.event_obj), GenericEventsManager.EventObject)
        self.assertFalse(response.created)