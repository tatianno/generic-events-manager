class GenericObject:
    
    def __init__(self, data) -> None:
        self.state = data['state'] if 'state' in data else None
        self.key = data['key'] if 'key' in data else None
    
    def get_key(self):
        return self.key