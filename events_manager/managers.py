from datetime import datetime
from events_manager.exceptions import ObjectDoesExists, ObjectWithoutGetKeyMethod
from events_manager.entities import GenericObject, GenericObserver


class GenericEventsManager():

    class EventObject(GenericObject):
        observer_class = GenericObserver
        last_state = None
        last_update = datetime.now()
    
    def __init__(self):
        self._objects_dict = {}

    def _observers_obj_update_event(self, new_obj: EventObject, old_obj: EventObject) -> None:
        
        for observer in new_obj.observers:
            observer._exec_routine_update_obj(new_obj, old_obj)
    
    def _observers_obj_delete_event(self, obj: EventObject) -> None:
        
        for observer in obj.observers:
            observer._exec_routine_delete_obj(obj)
    
    def get_update_obj(self, new_obj: EventObject, old_obj: EventObject) -> EventObject:
        new_obj.observers = old_obj.observers
        new_obj.last_state = old_obj.state
        new_obj.last_update = datetime.now()
        return new_obj

    def objects_factory(self, data: dict)-> EventObject:
        return self.EventObject(data)

    def perfom_create(self, new_obj: EventObject) -> None:
        self._objects_dict[new_obj.get_key()] = new_obj

    def perfom_update(self, new_obj: EventObject, old_obj: EventObject) -> None:
        self._objects_dict[new_obj.get_key()] = self.get_update_obj(new_obj, old_obj)
        self._observers_obj_update_event(new_obj, old_obj)
    
    def perfom_destroy(self, obj: EventObject) -> None:
        del self._objects_dict[obj.get_key()]
        self._observers_obj_delete_event(obj)

    def exists(self, obj_key: str) -> EventObject:
        return obj_key  in self._objects_dict
    
    def all(self) -> list:
        return [self._objects_dict[key] for key in self._objects_dict]
        
    def get(self, obj_key: str) -> EventObject:
        if not self.exists(obj_key):
            raise ObjectDoesExists(f'obj_key {obj_key} not exists')
        
        return self._objects_dict[obj_key]
    
    def create(self, new_obj: EventObject) -> None:
        self.perfom_create(new_obj)

    def update(self, new_obj: EventObject) -> None:
        old_obj = self.get(new_obj.get_key())
        self.perfom_update(new_obj, old_obj)
    
    def delete(self, obj: EventObject) -> None:
        self.perfom_destroy(obj)
    
    def get_factory_object(self, data: dict) -> EventObject:
        new_obj = self.objects_factory(data)

        if not hasattr(new_obj, 'get_key'):
            raise ObjectWithoutGetKeyMethod('Object without get key method implemeted')
        
        return new_obj
    
    def event_update(self, data: dict) -> None:
        new_obj = self.get_factory_object(data)

        if not self.exists(new_obj.get_key()):
            self.create(new_obj)
        
        else:
            self.update(new_obj)