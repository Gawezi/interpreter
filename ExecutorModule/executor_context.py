

from types import ClassMethodDescriptorType


class executor_context:
    def __init__(self,functions,classes,variables):
        self.functions=functions
        self.classes=classes
        self.variables=variables

    def __init__(self,context):
        self.functions=context.functions
        self.classes=context.classes
        self.variables=context.variables