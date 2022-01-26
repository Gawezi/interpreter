from ValidatorModule.defined_objects import *
from ParserModule.definitions import *
from ValidatorModule.validator_context import validator_context
from enum import Enum


std_functions={"print_int": defined_function(function_definition("print_int", "void", parameter("parameter","int"),[]), validator_context({},{})),
            "print_int": defined_function(function_definition("print_string", "void", parameter("parameter","string"),[]), validator_context({},{})),
            "print_int": defined_function(function_definition("print_bool", "void", parameter("parameter","bool"),[]), validator_context({},{}))
            }

std_names=["main"]

class std_type(Enum):
    Int="int"
    Bool="bool"
    string="string"
    void="void"
    