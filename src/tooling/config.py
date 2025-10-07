from typing import Callable, List


class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Config(metaclass=SingletonMeta):
    groups = {}

    def __init__(self):
        self.groups = {}

    def append(self, group_name: str, func: Callable):
        if group_name not in self.groups:
            self.groups[group_name] = [func]
            return 
        
        self.groups[group_name].append(func)

    def get_groups(self):
        print(self.groups)
        return self.groups
    
    def get(self, group_name: str) -> List[Callable]:
        try:
            return self.groups[group_name]
        except KeyError:
            return []