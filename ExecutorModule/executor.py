from ExecutorModule.executor_context import executor_context
from ValidatorModule.validator import IVisitor

class executor(IVisitor):
    def __init__(self):
        super().__init__()
        self.variable_to_return=None    

    def execute_program(self,program):
        self.execute_function(next(f for f in program.functions if f.name=="main"),executor_context(program.functions, program.classes,{}))

    def execute_function(self, function, scope_context):
        pass
    def execute_instructions_block(self,instructions, scope_context):
        for i in instructions:
            i.accept_executor(self,scope_context)


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