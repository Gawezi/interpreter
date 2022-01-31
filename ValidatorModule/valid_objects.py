from ParserModule.definitions import *
from ParserModule.parser_instance import program_instance
from ValidatorModule.defined_objects import defined_function

class valid_class:
    def __init__(self, defined_class):
        self.name=defined_class.name
        self.constructor=defined_class.constructor
        self.methods={i: valid_function(defined_class.functions[i]) for i in defined_class.functions.keys()}
        self.properties={i: defined_class.properties[i] for i in defined_class.properties.keys()}

class valid_function(function_definition): 
    def __init__(self, defined_function: defined_function):
        super().__init__(defined_function.name, defined_function.type, defined_function.parameters, defined_function.instructions)

class valid_program:
    def __init__(self, classes: valid_class, functions: valid_function):
        self.valid_functions=functions
        self.valid_classes=classes