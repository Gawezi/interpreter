from ParserModule.instructions import function_call_instruction
from ParserModule.node_interface import Node

class expression(Node):
    def accept_validator(self,validator_visitor, validator_context):
        pass
    def accept_executor(self,executor_visitor, executor_context):
        pass


class additive_expression(expression):
    def __init__(self, type, left,right):
        super().__init__()
        self.type=type
        self.left=left
        self.right=right

    def accept_validator(self,validator_visitor, validator_context):
        validator_visitor.visit_additive_expression(validator_visitor, validator_context)

    def accept_executor(self,executor_visitor, executor_context):
        executor_visitor.visit_additive_expression(executor_visitor, executor_context)


class and_expression(expression):
    def __init__(self, left,right):
        super().__init__()
        self.left=left
        self.right=right

    def accept_validator(self,validator_visitor, validator_context):
        validator_visitor.visit_and_expression(validator_visitor, validator_context)

    def accept_executor(self,executor_visitor, executor_context):
        executor_visitor.visit_and_expression(executor_visitor, executor_context)


class multiplicative_expression(expression):
    def __init__(self, type, left,right):
        super().__init__()
        self.type=type
        self.left=left
        self.right=right

    def accept_validator(self,validator_visitor, validator_context):
        validator_visitor.visit_multiplicative_expression(validator_visitor, validator_context)

    def accept_executor(self,executor_visitor, executor_context):
        executor_visitor.visit_multiplicative_expression(executor_visitor, executor_context)

class not_expression(expression):
    def __init__(self, left, is_negated):
        super().__init__()
        self.left=left
        self.is_negated=is_negated
        self.right=None

    def accept_validator(self,validator_visitor, validator_context):
        validator_visitor.visit_not_expression(validator_visitor, validator_context)

    def accept_executor(self,executor_visitor, executor_context):
        executor_visitor.visit_not_expression(executor_visitor, executor_context)

class or_expression(expression):
    def __init__(self, left,right):
        super().__init__()
        self.left=left
        self.right=right

    def accept_validator(self,validator_visitor, validator_context):
        validator_visitor.visit_or_expression(validator_visitor, validator_context)

    def accept_executor(self,executor_visitor, executor_context):
        executor_visitor.visit_or_expression(executor_visitor, executor_context)

class relative_expression(expression):
    def __init__(self, type, left,right):
        super().__init__()
        self.type=type
        self.left=left
        self.right=right

    def accept_validator(self,validator_visitor, validator_context):
        validator_visitor.visit_relative_expression(validator_visitor, validator_context)

    def accept_executor(self,executor_visitor, executor_context):
        executor_visitor.visit_relative_expression(executor_visitor, executor_context)

class function_call_expression(expression):
    def __init__(self, name, arguments):
        super().__init__()
        self.name=name
        self.arguments=arguments

    def accept_validator(self,validator_visitor, validator_context):
        validator_visitor.visit_function_call_expression(validator_visitor, validator_context)

    def accept_executor(self,executor_visitor, executor_context):
        executor_visitor.visit_function_call_expression(executor_visitor, executor_context)

class method_call_expression(expression):
    def __init__(self, name, function_call_instruction:function_call_instruction):
        super().__init__()
        self.object_name=name
        self.function=function_call_instruction

    def accept_validator(self,validator_visitor, validator_context):
        validator_visitor.visit_method_call_expression(validator_visitor, validator_context)

    def accept_executor(self,executor_visitor, executor_context):
        executor_visitor.visit_method_call_expression(executor_visitor, executor_context)

class property_call_expression(expression):
    def __init__(self, object_name, property_name):
        super().__init__()
        self.object_name=object_name
        self.property_name=property_name

    def accept_validator(self,validator_visitor, validator_context):
        validator_visitor.visit_property_call_expression(validator_visitor, validator_context)

    def accept_executor(self,executor_visitor, executor_context):
        executor_visitor.visit_property_call_expression(executor_visitor, executor_context)

class bool_literal_expression(expression):
    def __init__(self,value):
        super().__init__()
        self.value=value
    def accept_validator(self,validator_visitor, validator_context):
        validator_visitor.visit_bool_literal_expression(validator_visitor, validator_context)

    def accept_executor(self,executor_visitor, executor_context):
        executor_visitor.visit_bool_literal_expression(executor_visitor, executor_context)


class int_literal_expression(expression):
    def __init__(self,value):
        super().__init__()
        self.value=value

    def accept_validator(self,validator_visitor, validator_context):
        validator_visitor.visit_int_literal_expression(validator_visitor, validator_context)

    def accept_executor(self,executor_visitor, executor_context):
        executor_visitor.visit_int_literal_expression(executor_visitor, executor_context)

class string_literal_expression(expression):
    def __init__(self,value):
        super().__init__()
        self.value=value

    def accept_validator(self,validator_visitor, validator_context):
        validator_visitor.visit_string_literal_expression(validator_visitor, validator_context)

    def accept_executor(self,executor_visitor, executor_context):
        executor_visitor.visit_string_literal_expression(executor_visitor, executor_context)

class variable_expression(expression):
    def __init__(self,name):
        super().__init__()
        self.name=name

    def accept_validator(self,validator_visitor, validator_context):
        validator_visitor.visit_variable_expression(validator_visitor, validator_context)

    def accept_executor(self,executor_visitor, executor_context):
        executor_visitor.visit_variable_expression(executor_visitor, executor_context)

