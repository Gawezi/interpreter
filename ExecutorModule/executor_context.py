

from types import ClassMethodDescriptorType

def create_copy_of_dict(dict):
    return {key: value for key,value in dict.items()}

class executor_context:

    def __init__(self):
        self.functions={}
        self.classes={}
        self.variables={}