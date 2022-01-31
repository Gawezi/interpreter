from unicodedata import name
from ParserModule.definitions import *

def create_copy_of_dict(dict):
    return {key: value for key,value in dict.items()}
class defined_class(class_definition):
    def __init__(self, class_definition, validator_context):
        super().__init__(class_definition.name,class_definition.constructor, class_definition.functions, class_definition.properties)
        self.defined_properties={i: defined_variable(class_definition.properties[i].name,class_definition.properties[i].type) for i in class_definition.properties.keys()}

        #self.defined_properties={class_definition.properties[i].name: defined_variable(class_definition.properties[i].name,class_definition.properties[i].type) for i in range(0,len(class_definition.properties))}
        #self.defined_methods={class_definition.properties[i].name: defined_variable(class_definition.functions[i].name,class_definition.functions[i].type) for i in range(0,len(class_definition.functions))}
        self.defined_methods={i: defined_variable(class_definition.functions[i].name,class_definition.functions[i].type) for i in class_definition.functions.keys()}
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