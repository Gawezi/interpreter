from ParserModule.definitions import *
from ParserModule.parser_instance import program_instance
from ValidatorModule.defined_objects import defined_function

class valid_class:
    def __init__(self, name, constructor, functions, properties):
        self.name=name
        self.constructor=constructor
        self.methods=functions
        self.properties=properties

    def __init__(self, defined_class):
        self.name=defined_class.name
        self.constructor=defined_class.constructor
        self.methods={defined_class.functions[i].name: valid_function(defined_class.functions[i]) for i in range(0,len(defined_class.functions))}
        self.properties={defined_class.properties[i].name: defined_class.properties[i] for i in range(0,len(defined_class.properties))}

class valid_function(function_definition):
    def __init__(self, name, type, parameters, instructions):
        super().__init__(name, type, parameters, instructions)
    
    def __init__(self, defined_function: defined_function):
        super().__init__(defined_function.name, defined_function.type, defined_function.parameters, defined_function.instructions)

class valid_program:
    def __init__(self, classes: valid_class, functions: valid_function):
        self.valid_functions=functions
        self.valid_classes=classes

    def __init__(self):
        super().__init__()
        self.valid_functions={}
        self.valid_classes={}