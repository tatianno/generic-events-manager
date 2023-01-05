from events_manager.exceptions import ObjectDoesExists ,ObjectsFactoryNotDefined, ObjectWithoutGetKeyMethod
from events_manager.entities import GenericObject


class GenericEventsManager:
    _objects_dict = {}
    objects_factory = None

    def __init__(self) -> None:
        if not self.objects_factory:
            raise ObjectsFactoryNotDefined('objects_factory not defined')

    def _exec_routine_before_create_new_obj(self, obj: GenericObject) -> None:
        ...
    
    def _exec_routine_after_create_new_obj(self, obj: GenericObject) -> None:
        ...
    
    def _exec_routine_before_update_obj(self, obj_new_state: GenericObject, obj_old_state: GenericObject) -> None:
        ...
    
    def _exec_routine_after_update_obj(self, obj_new_state: GenericObject, obj_old_state: GenericObject) -> None:
        ...
    
    def _exec_routine_before_delete_obj(self, obj_new_state: GenericObject, obj_old_state: GenericObject) -> None:
        ...
    
    def _exec_routine_after_delete_obj(self, obj_new_state: GenericObject, obj_old_state: GenericObject) -> None:
        ...
    
    def perfom_create(self, new_obj: GenericObject) -> None:
        self._exec_routine_before_create_new_obj(new_obj)
        self._objects_dict[new_obj.get_key()] = self.perfom_create(new_obj)
        self._exec_routine_after_create_new_obj(new_obj)

    def perfom_update(self, new_obj: GenericObject, old_obj: GenericObject) -> None:
        self._exec_routine_before_update_obj(new_obj, old_obj)
        self._objects_dict[new_obj.get_key()] = self.perfom_update(new_obj, old_obj)
        self._exec_routine_after_update_obj(new_obj, old_obj)
    
    def perfom_destroy(self, obj: GenericObject) -> None:
        self._exec_routine_before_delete_obj(obj)
        del self._objects_dict[obj.get_key()]
        self._exec_routine_after_delete_obj(obj)
        
    def get(self, obj_key: str) -> GenericObject:
        if obj_key not in self._objects_dict:
            raise ObjectDoesExists(f'obj_key {obj_key} not exists')
        
        return self._objects_dict[obj_key]

    def create(self, new_obj: GenericObject) -> None:
        self.perfom_create(new_obj)

    def update(self, new_obj: GenericObject) -> None:
        old_obj = self.get(new_obj.get_key())
        self.perfom_update(new_obj, old_obj)
    
    def delete(self, obj: GenericObject) -> None:
        self.perfom_destroy(obj)
    
    def get_factory_object(self, data: dict) -> GenericObject:
        new_obj = self.objects_factory(data)

        if not hasattr(new_obj, 'get_key'):
            raise ObjectWithoutGetKeyMethod('Object without get key method implemeted')
        
        return new_obj
    
    def event_update(self, data: dict) -> None:
        new_obj = self.get_factory_object(data)

        if new_obj.get_key() not in self._objects_dict:
            self.create(new_obj)
        
        else:
            self.update(new_obj)