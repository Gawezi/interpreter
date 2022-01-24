from ValidatorModule.validator_context import *
from ValidatorModule.valid_objects import *
class IVisitor:
#region INSTRUCTION_VISITORS
    def visit_var_declaration_instruction(self,variable_declaration, scope_context):
        "jest to interfejs"

    def visit_assignment_instruction(self,assignment, scope_context):
        "jest to interfejs"

    def visit_function_call_instruction(self,function_call, scope_context):
        "jest to interfejs"

    def visit_method_call_instruction(self,method_call, scope_context):
        "jest to interfejs"

    def visit_return_instruction(self,return_instruction, scope_context):
        "jest to interfejs"

    def visit_if_else_instruction(self,if_else_instruction, scope_context):
        "jest to interfejs"

    def visit_while_instruction(self,while_instruction, scope_context):
        "jest to interfejs"
#endregion


#region EXPRESSION_VISITOR
    def visit_or_expression(or_expression, scope_context):
        "jest to interfejs"

    def visit_and_expression(and_expression, scope_context):
        "jest to interfejs"

    def visit_relative_expression(relative_expression, scope_context):
        "jest to interfejs"

    def visit_additive_expression(additive_expression, scope_context):
        "jest to interfejs"

    def visit_multiplicative_expression(multiplicative_expression, scope_context):
        "jest to interfejs"

    def visit_not_expression(not_expression, scope_context):
        "jest to interfejs"

    def visit_variable_expression(variable_expression, scope_context):
        "jest to interfejs"

    def visit_property_call_expression(property_call_expression, scope_context):
        "jest to interfejs"

    def visit_method_call_expression(method_call_expression, scope_context):
        "jest to interfejs"

    def visit_function_call_expression(function_call_expression, scope_context):
        "jest to interfejs"

    def visit_int_literal_expression(int_literal_expression, scope_context):
        "jest to interfejs"

    def visit_bool_literal_expression(bool_literal_expression, scope_context):
        "jest to interfejs"

    def visit_string_literal_expression(string_literal_expression, scope_context):
        "jest to interfejs"
#endregion

class validator(IVisitor):
    def __init__(self, error_handler):
        super().__init__()
        self.error_handler=error_handler
        self.defined_classes={}
        self.defined_functions={}
        self.current_function_type=None

    def validate_program(self, program_instance):
        for c in program_instance.classes:
            self.validate_class_definition_header(c)
        
        for f in program_instance.functions:
            self.validate_function_definition_header(f)
        
        self.validate_main()

        for f in self.defined_functions.values():
            self.current_function_type=f.type
            context=validator_context(f.validator_context)
            context.defined_functions=self.defined_functions
            self.validate_instructions_block(f.instructions, context)

        for c in self.defined_classes.values():
            self.validate_class_definition(c)

        if(len(self.error_handler.error_messages)>0):
            self.error_handler.stop_everything()
        
        return True
    
    def validate_class_definition_header(self, class_definition):
        if(class_definition.name in self.defined_classes.keys()):
            self.error_handler.add_error("Multiple definitions of class with name: "+class_definition.name)
        if(class_definition.name in ["bool", "int", "string", "void"]):
            self.error_handler.add_error("Class cannot have name: "+class_definition.name)
            


        



#region INSTRUCTION_VISITORS
    def visit_var_declaration_instruction(self,variable_declaration, scope_context):
        "jest to interfejs"

    def visit_assignment_instruction(self,assignment, scope_context):
        "jest to interfejs"

    def visit_function_call_instruction(self,function_call, scope_context):
        "jest to interfejs"

    def visit_method_call_instruction(self,method_call, scope_context):
        "jest to interfejs"

    def visit_return_instruction(self,return_instruction, scope_context):
        "jest to interfejs"

    def visit_if_else_instruction(self,if_else_instruction, scope_context):
        "jest to interfejs"

    def visit_while_instruction(self,while_instruction, scope_context):
        "jest to interfejs"
#endregion

#region EXPRESSION_VISITOR
    def visit_or_expression(or_expression, scope_context):
        "jest to interfejs"

    def visit_and_expression(and_expression, scope_context):
        "jest to interfejs"

    def visit_relative_expression(relative_expression, scope_context):
        "jest to interfejs"

    def visit_additive_expression(additive_expression, scope_context):
        "jest to interfejs"

    def visit_multiplicative_expression(multiplicative_expression, scope_context):
        "jest to interfejs"

    def visit_not_expression(not_expression, scope_context):
        "jest to interfejs"

    def visit_variable_expression(variable_expression, scope_context):
        "jest to interfejs"

    def visit_property_call_expression(property_call_expression, scope_context):
        "jest to interfejs"

    def visit_method_call_expression(method_call_expression, scope_context):
        "jest to interfejs"

    def visit_function_call_expression(function_call_expression, scope_context):
        "jest to interfejs"

    def visit_int_literal_expression(int_literal_expression, scope_context):
        "jest to interfejs"

    def visit_bool_literal_expression(bool_literal_expression, scope_context):
        "jest to interfejs"

    def visit_string_literal_expression(string_literal_expression, scope_context):
        "jest to interfejs"
#endregion