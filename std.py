from ValidatorModule.defined_objects import *
from ParserModule.definitions import *
from ValidatorModule.validator_context import validator_context
from enum import Enum


std_functions={"printint": defined_function(function_definition("printint", "void", [parameter("parameter","int")],[]), validator_context()),
            "printstring": defined_function(function_definition("printstring", "void", [parameter("parameter","string")],[]), validator_context()),
            "printbool": defined_function(function_definition("printbool", "void", [parameter("parameter","bool")],[]), validator_context())
            }

std_names=["main"]

class std_type(Enum):
    Int="int"
    Bool="bool"
    string="string"
    void="void"
