from events_manager.exceptions import InvalidObserver


class GenericObserver:

    def __init__(self):
        ...
    
    def _exec_routine_update_obj(self, obj_new_state, obj_old_state) -> None:
        ...
    
    def _exec_routine_delete_obj(self, obj) -> None:
        ...
    

class GenericObject:
    observer_class = GenericObserver
    
    def __init__(self, data) -> None:
        self.state = data['state'] if 'state' in data else None
        self.key = data['key'] if 'key' in data else None
        self.observers = []

    def get_key(self) -> str:
        return self.key
    
    def validate_observer(self, observer: observer_class) -> bool:
        if type(observer) != self.observer_class:
            raise InvalidObserver(f"observer cannot be of type {type(observer)}")
        
        return True

    def subscribe(self, observer: observer_class) -> None:
        self.validate_observer(observer)
        self.observers.append(observer)
    
    def unsubscribe(self, observer: observer_class) -> None:
        self.validate_observer(observer)
        self.observers.remove(observer)
    
    def unsubscribe_all(self) -> None:
        self.observers = []


