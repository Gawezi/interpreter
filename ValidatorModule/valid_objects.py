from ParserModule.definitions import *
from ParserModule.parser import program_instance

class valid_class(class_definition):
    def __init__(self, name, constructor, functions, properties):
        super().__init__(name, constructor, functions, properties)

class valid_function(function_definition):
    def __init__(self, name, type, parameters, instructions):
        super().__init__(name, type, parameters, instructions)

class valid_program(program_instance):
    def __init__(self, functions, classes):
        super().__init__(functions, classes)

    def __init__(self):
        super().__init__()
        self.valid_functions={}
        self.valid_classes={}