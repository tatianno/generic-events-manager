from events_manager import GenericEventsManager
from events_manager.entities import GenericObserver


class CustomObserver(GenericObserver):

    def _exec_routine_update_obj(self, obj_new: GenericEventsManager.EventObject, obj_old: GenericEventsManager.EventObject) -> None:
        print(f'The object {obj_new.key} has been updated with the state {obj_new.state}')
        print(f'The previous state was {obj_old.state}')
        
    def _exec_routine_delete_obj(self, obj: GenericEventsManager.EventObject) -> None:
        print(f'The object {obj.key} has been deleted')


class CustomEventsManager(GenericEventsManager):

    class EventObject(GenericEventsManager.EventObject):
        observer_class = CustomObserver
    
    def create(self, entity: EventObject) -> None:
        self.perfom_create(entity)

    def update(self, entity: EventObject) -> None:
        old_entity = self.get(entity.get_key())
        self.perfom_update(entity, old_entity)
    
    def delete(self, entity: EventObject) -> None:
        self.perfom_destroy(entity)


events_manager = CustomEventsManager()
observer = CustomObserver()
data = {
    'state' : 'ON',
    'key' : 'k1'
}
response = events_manager.event_update(data)
obj = events_manager.get('k1')
obj.subscribe(observer)
data = {
    'state' : 'OFF',
    'key' : 'k1'
}
response = events_manager.event_update(data)
obj = events_manager.get('k1')
events_manager.delete(obj)
