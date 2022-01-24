from parser import Node


class instruction(Node):
    def accept_validator(self,validator_visitor, validator_context):
        pass
    def accept_executor(self,executor_visitor, executor_context):
        pass



class assignment_instruction(instruction):
    def __init__(self,variable_name,expression):
        super().__init__()
        self.variable_name=variable_name
        self.expression=expression

    def accept_validator(self,validator_visitor, validator_context):
        validator_visitor.visit_assignment_instruction(validator_visitor, validator_context)

    def accept_executor(self,executor_visitor, executor_context):
        executor_visitor.visit_assignment_instruction(executor_visitor, executor_context)

class function_call_instruction(instruction):
    def __init__(self,name,arguments):
        super().__init__()
        self.name=name
        self.arguments=arguments
    def accept_validator(self,validator_visitor, validator_context):
        validator_visitor.visit_function_call_instruction(validator_visitor, validator_context)

    def accept_executor(self,executor_visitor, executor_context):
        executor_visitor.visit_function_call_instruction(executor_visitor, executor_context)


class if_else_instruction(instruction):
    def __init__(self,condition,if_instructions, else_instructions):
        super().__init__()
        self.condition=condition
        self.if_instructions=if_instructions
        self.else_instructions=else_instructions

    def accept_validator(self,validator_visitor, validator_context):
        validator_visitor.visit_if_else_instruction(validator_visitor, validator_context)

    def accept_executor(self,executor_visitor, executor_context):
        executor_visitor.visit_if_else_instruction(executor_visitor, executor_context)


class method_call_instruction(instruction):
    def __init__(self,object_name,function):
        super().__init__()
        self.object_name=object_name
        self.function=function

    def accept_validator(self,validator_visitor, validator_context):
        validator_visitor.visit_method_call_instruction(validator_visitor, validator_context)

    def accept_executor(self,executor_visitor, executor_context):
        executor_visitor.visit_method_call_instruction(executor_visitor, executor_context)


# class property_call_instruction(instruction):
#     def __init__(self,object_name,property_name):
#         super().__init__()
#         self.object_name=object_name
#         self.property_name=property_name

#     def accept_validator(self,validator_visitor, validator_context):
#         validator_visitor.visit_property_call_instruction(validator_visitor, validator_context)

#     def accept_executor(self,executor_visitor, executor_context):
#         executor_visitor.visit_property_call_instruction(executor_visitor, executor_context)


class return_instruction(instruction):
    def __init__(self,expression):
        super().__init__()
        self.expression=expression

    def accept_validator(self,validator_visitor, validator_context):
        validator_visitor.visit_return_instruction(validator_visitor, validator_context)

    def accept_executor(self,executor_visitor, executor_context):
        executor_visitor.visit_return_instruction(executor_visitor, executor_context)


class variable_declaration_instruction(instruction):
    def __init__(self,name,type,expression):
        super().__init__()
        self.name=name
        self.type=type
        self.expression=expression

    def accept_validator(self,validator_visitor, validator_context):
        validator_visitor.visit_variable_declaration_instruction(validator_visitor, validator_context)

    def accept_executor(self,executor_visitor, executor_context):
        executor_visitor.visit_variable_declaration_instruction(executor_visitor, executor_context)


class while_instruction(instruction):
    def __init__(self,condition,instructions):
        super().__init__()
        self.condition=condition
        self.instructions=instructions

    def accept_validator(self,validator_visitor, validator_context):
        validator_visitor.visit_while_instruction(validator_visitor, validator_context)

    def accept_executor(self,executor_visitor, executor_context):
        executor_visitor.visit_while_instruction(executor_visitor, executor_context)
