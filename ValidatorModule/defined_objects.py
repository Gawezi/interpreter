from unicodedata import name
from ParserModule.definitions import *

class defined_class(class_definition):
    def __init__(self, class_definition, defined_properties, defined_methods, validator_context):
        super().__init__(class_definition.name, class_definition.constructor, class_definition.functions, class_definition.properties)
        self.defined_properties=defined_properties
        self.defined_methods=defined_methods
        self.validator_context=validator_context

class defined_function(function_definition):
    def __init__(self, function_definition, validator_context):
        super().__init__(function_definition.name, function_definition.type, function_definition.parameters, function_definition.instructions)
        self.validator_context=validator_context

class defined_variable:
    def __init__(self, name, type, is_initialized=False):
        self.type=type
        self.name=name
        self.is_initialized=is_initialized