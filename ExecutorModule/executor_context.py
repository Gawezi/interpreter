

from types import ClassMethodDescriptorType

def create_copy_of_dict(dict):
    return {key: value for key,value in dict.items()}

class executor_context:
    def __init__(self,functions,classes,variables):
        self.functions=create_copy_of_dict(functions)
        self.classes=create_copy_of_dict(classes)
        self.variables=create_copy_of_dict(variables)

    def __init__(self,context):
        self.functions=create_copy_of_dict(context.functions)
        self.classes=create_copy_of_dict(context.classes)
        self.variables=create_copy_of_dict(context.variables)