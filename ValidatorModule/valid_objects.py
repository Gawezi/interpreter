from ParserModule.definitions import *
from ParserModule.parser import program_instance

class valid_class:
    def __init__(self, name, constructor, functions, properties):
        self.name=name
        self.constructor=constructor
        self.functions=functions
        self.properties=properties

    def __init__(self, defined_class):
        self.name=defined_class.name
        self.constructor=defined_class.constructor
        self.functions={defined_class.functions[i].name: valid_function(defined_class.functions[i]) for i in range(0,len(defined_class.functions))}
        self.properties={defined_class.properties[i].name: defined_class.properties[i] for i in range(0,len(defined_class.properties))}

class valid_function(function_definition):
    def __init__(self, name, type, parameters, instructions):
        super().__init__(name, type, parameters, instructions)

class valid_program:
    def __init__(self, classes, functions):
        self.functions=functions
        self.classes=classes

    def __init__(self):
        super().__init__()
        self.valid_functions={}
        self.valid_classes={}