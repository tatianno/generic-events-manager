#  GenericEventsManager

## Overview

It is a generic class for managing events generated by an application.


## Installing GenericEventsManager and Supported Versions

GenericEventsManager is available on PyPI:

`$ python -m pip install generic-events-manager`

GenericEventsManager officially supports Python 3.8+.

## Cloning the repository

`$ git clone https://github.com/tatianno/generic-events-manager.git`

## Example

```
from events_manager import GenericEventsManager
from events_manager.entities import GenericObserver


class CustomObserver(GenericObserver):

    def _exec_routine_update_obj(self, obj_new: GenericEventsManager.EventObject, obj_old: GenericEventsManager.EventObject) -> None:
        '''
        Method called each time the observed object changes state
        '''
        print(f'The object {obj_new.key} has been updated with the state {obj_new.state}')
        print(f'The previous state was {obj_old.state}')
        
    def _exec_routine_delete_obj(self, obj: GenericEventsManager.EventObject) -> None:
        '''
        Method called when observed object is deleted
        '''
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


# Instantiating the Event Handler and Observer
events_manager = CustomEventsManager()
observer = CustomObserver()

# Dictionary containing event data
data = {
    'state' : 'ON',
    'key' : 'k1'
}

# Updating the object with the received event data
response = events_manager.event_update(data)

# Subscribing observer
obj = events_manager.get('k1')
obj.subscribe(observer)

# Dictionary containing event data
data = {
    'state' : 'OFF',
    'key' : 'k1'
}

# Updating the object with the received event data
response = events_manager.event_update(data)

# Deleting object
obj = events_manager.get('k1')
events_manager.delete(obj)
```
