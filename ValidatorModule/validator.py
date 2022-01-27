from ParserModule.expressions import *
from ParserModule.instructions import *
from ValidatorModule.defined_objects import *
from ValidatorModule.validator_context import *
from ValidatorModule.valid_objects import *
import std
from error_handler import *
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
    def __init__(self, error_handler :error_handler):
        super().__init__()
        self.error_handler=error_handler
        self.defined_classes={}
        self.defined_functions={}
        self.std_functions=std.std_functions
        self.current_function_type=None

    def is_type_defined(self, type):
        return (type == std.std_type.Bool.value or type== std.std_type.Int.value or type in self.defined_classes.keys())

    def validate_program(self, program_instance: program_instance):
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
        

 
        classes={}
        functions={}
        for key in self.defined_classes.keys():
            classes[key]=valid_class(self.defined_classes[key])
        for key in self.defined_functions.keys():
            functions[key]=valid_function(self.defined_functions[key])

        return valid_program(classes,functions)
    
    def validate_class_definition_header(self, class_definition: class_definition):
        is_ok=True
        if(class_definition.name in self.defined_classes.keys()):
            self.error_handler.add_error("Multiple definitions of class with name: "+class_definition.name)
        if(class_definition.name in std.std_names):
            self.error_handler.add_error("Class cannot have name: "+class_definition.name)
            is_ok=False            

        defined_properties={}

        for key in class_definition.properties.keys():
            property=class_definition.properties[key]
            if(not self.is_type_defined(property.type)):
                self.error_handler.add_error("Declaration of property"+ property.name + "is with unknown type"+ property.type +" in class "+ class_definition.name)
            if(property.name in defined_properties.keys()):
                self.error_handler.add_error("Multiple definitions of property with name: "+property.name+" in class "+ class_definition.name)

            if(property.expression is not None):
                expression_type=property.expression.accept_validator(self, validator_context())
                if(property.type!= expression_type):
                    self.error_handler.add_error("Cannot assign expression of type"+expression_type+" to property"+property.name+ "in class "+ class_definition.name)
            defined_properties[property.name]=defined_variable(property.name,property.type,True)
        
        defined_methods={}
        for key in class_definition.functions.keys():
            property=class_definition.functions[key]
            if(not self.is_type_defined(property.type) and property.type!="void"):
                self.error_handler.add_error("Declaration of method"+ property.name + "is with unknown type"+ property.type +" in class "+ class_definition.name)
            if(property.name in defined_methods.keys()):
                self.error_handler.add_error("Multiple definitions of function with name: "+property.name+" in class "+ class_definition.name)

            if(property.name in std.std_functions.keys()):
                self.error_handler.add_error("Cannot redefine standard function"+property.name + "in class: "+class_definition.name)

            function_context=validator_context()
            for parameter in property.parameters:
                if(not self.is_type_defined(parameter.type)):
                    self.error_handler.add_error(f"Unknown parameter type: {parameter.type} of name: {parameter.name} in method {property.name} in class {class_definition.name}")
                if(parameter.name in defined_properties.keys()):
                    self.error_handler.add_error(f"Parameter {parameter.name} in conflict with property in method {property.name} in class {class_definition.name}")
                if(parameter.name in function_context.defined_variables.keys()):
                    self.error_handler.add_error(f"Multiple definitions of parameters {parameter.name} in method {property.name} in class {class_definition.name}")
                function_context.defined_variables[parameter.name]=defined_variable(parameter.name,parameter.type,True)
            function_context.defined_functions[property.name]=defined_function(property,function_context)

        for function in defined_methods.values():
            function.validator_context.defined_functions=defined_methods
            for key in defined_properties.keys(): 
                function.validator_context.defined_variables[key]=defined_properties[key]

        constructor_context=validator_context()

        for parameter in class_definition.constructor.parameters:
            if(not self.is_type_defined(parameter.type)):
                self.error_handler.add_error(f"Unknown type {parameter.type} for constructor of class {class_definition.name}")
            if(parameter.name in constructor_context.defined_variables.keys()):
                self.error_handler.add_error(f"Multiple usage of parameter name {parameter.name} in constructor of class {class_definition.name}")
            if(not parameter.name in defined_properties.keys() and not parameter.name in constructor_context.defined_variables.keys()):
                constructor_context.defined_variables[parameter.name]=defined_variable(parameter.name, parameter.type,True)
        for key in defined_properties.keys(): 
            constructor_context.defined_variables[key]=defined_properties[key]

        if(is_ok):
            self.defined_classes[class_definition.name]=defined_class(class_definition, constructor_context)
            self.defined_classes[class_definition.name].defined_methods=defined_methods
            self.defined_classes[class_definition.name].defined_properties=defined_properties

    def validate_function_definition_header(self, function_definition: function_definition):
        if(not self.is_type_defined(function_definition.type) and function_definition.type!="void"):
            self.error_handler.add_error(f"Function {function_definition.name} returns unknown type {function_definition.type}")
        is_redefinition=False
        if(function_definition.name in self.defined_functions.keys()):
            self.error_handler.add_error(f"Multiple functions with name {function_definition.name}")
            is_redefinition=True
        if(function_definition.name in std.std_functions.keys()):
            self.error_handler.add_error(f"You cannnot use standart library function names {function_definition.name}")
            is_redefinition=True
        
        context=validator_context()
        for parameter in function_definition.parameters:
            if(not self.is_type_defined(parameter.type)):
                self.error_handler.add_error(f"Unknown type {parameter.type} of parameter {parameter.name} in function {function_definition.name}")
            if(parameter.name in context.defined_variables.keys()):
                self.error_handler.add_error(f"Multiple parameters with name {parameter.name} in function {function_definition.name}")
            context.defined_variables[parameter.name]=defined_variable(parameter.name,parameter.type,True)
        if(not is_redefinition):
            self.defined_functions[function_definition.name]= defined_function(function_definition,context )

    def validate_main(self):
        if("main" not in self.defined_functions.keys()):
            self.error_handler.add_error(f"No main function")
        main_function=self.defined_functions["main"]
        if(main_function is None or main_function.type!="void"):
            self.error_handler.add_error(f"Main function can bo only of type void")
        
        if(main_function is None or len(main_function.parameters) >0):
            self.error_handler.add_error("Main function cannot have parameters")
    
    def validate_instructions_block(self,instructions: list[instruction], validator_context:validator_context):
        for instruction in instructions:
            instruction.accept_validator(self, validator_context)

#region INSTRUCTION_VISITORS
    def visit_var_declaration_instruction(self,variable_declaration: variable_declaration_instruction, scope_context:validator_context):
        if(not self.is_type_defined(variable_declaration.type)):
            self.error_handler.add_error(f"Variable {variable_declaration.name} is unknown type {variable_declaration.type}")
        
        if(variable_declaration.name in scope_context.defined_variables.keys()):
            self.error_handler.add_error(f"Multiple declarations of variable {variable_declaration.name}")
        else:
            scope_context.defined_variables[variable_declaration.name]=defined_variable(variable_declaration.name, variable_declaration.type, True)

        if(variable_declaration.expression is None):
            return

        expression_type= variable_declaration.expression.accept_validator(self, scope_context)
        if(variable_declaration.type!=expression_type):
            self.error_handler.add_error(f"Cannot assign expression of type {expression_type} to variable {variable_declaration.name} with type {variable_declaration.type}")
        


    def visit_assignment_instruction(self,assignment: assignment_instruction, scope_context:validator_context):
        if(assignment.variable_name not in scope_context.defined_variables.keys()):
            self.error_handler.add_error(f"Assignment to undefined variable {assignment.variable_name}")
        
        variable=scope_context.defined_variables[assignment.variable_name]
        if(variable is None):
            return

        expression_type = assignment.expression.accept_validator(self, scope_context)
        if(variable.type != expression_type):
            self.error_handler.add_error(f"Not matching types of variable {variable.name} with type {variable.type} and corresponding to it assignment expression of type {expression_type}")

        variable.is_initialized=True



    def visit_function_call_instruction(self,function_call:function_call_instruction, scope_context:validator_context):
        self.validate_function_call(function_call, scope_context)
        #tu mozna dodac handlowanie warninga


    def visit_method_call_instruction(self,method_call:method_call_instruction, scope_context:validator_context):
        self.validate_method_call(method_call, scope_context)
        #tu mozna dodac warningi

    def visit_return_instruction(self,return_instruction:return_instruction, scope_context:validator_context):
        if(return_instruction.expression is not None):
            return_type=return_instruction.expression.accept_validator(self,scope_context)
        if(return_type!=self.current_function_type):
            self.error_handler.add_error(f"Cannot return expression type {return_type} from function that returns {self.current_function_type}")

    def visit_if_else_instruction(self,if_else_instruction:if_else_instruction, scope_context:validator_context):
        condition_type=if_else_instruction.condition.accept_validator(self, scope_context)
        if(condition_type!="bool"):
            self.error_handler.add_error(f"Condition in if is not type bool")
        self.validate_instructions_block(if_else_instruction.if_instructions,validator_context(scope_context))
        if(if_else_instruction.else_instructions is not None):
            self.validate_instructions_block(if_else_instruction.else_instructions,validator_context(scope_context))

    def visit_while_instruction(self,while_instruction:while_instruction, scope_context:validator_context):
        condition_type=while_instruction.condition.accept_validator(self, scope_context)
        if(condition_type!="bool"):
            self.error_handler.add_error(f"Condition in while is not type bool")
        self.validate_instructions_block(while_instruction.instructions,validator_context(scope_context))
#endregion

#region EXPRESSION_VISITOR
    def visit_or_expression(self,or_expression:or_expression, scope_context:validator_context):
        left_type=or_expression.left.accept_validator(self, scope_context)
        right_type=or_expression.right.accept_validator(self, scope_context)
        if(left_type!="bool" or right_type!="bool"):
            self.error_handler.add_error(f"Cannot apply or operator to types {left_type} and {right_type}")
        return "bool"

    def visit_and_expression(self,and_expression:and_expression, scope_context:validator_context):
        left_type=and_expression.left.accept_validator(self, scope_context)
        right_type=and_expression.right.accept_validator(self, scope_context)
        if(left_type!="bool" or right_type!="bool"):
            self.error_handler.add_error(f"Cannot apply and operator to types {left_type} and {right_type}")
        return "bool"

    def visit_relative_expression(self,relative_expression:relative_expression, scope_context:validator_context):
        left_type=relative_expression.left.accept_validator(self, scope_context)
        right_type=relative_expression.right.accept_validator(self, scope_context)
        if(left_type!=right_type or (left_type!="bool" and left_type!="int") or (left_type=="bool" and (relative_expression.type!="==" and relative_expression.type!="!="))):
            self.error_handler.add_error(f"Cannot apply operator {relative_expression.type} to expressions of type {left_type} and {right_type}")
        return "bool"

    def visit_additive_expression(self,additive_expression:additive_expression, scope_context:validator_context):
        left_type=additive_expression.left.accept_validator(self, scope_context)
        right_type=additive_expression.right.accept_validator(self, scope_context)
        if(left_type!="int" or right_type!="int"):
            self.error_handler.add_error(f"Cannont apply {additive_expression.type} operator to expressions of type diffrent than int")
        return "int"

    def visit_multiplicative_expression(self,multiplicative_expression:multiplicative_expression, scope_context:validator_context):
        left_type=multiplicative_expression.left.accept_validator(self, scope_context)
        right_type=multiplicative_expression.right.accept_validator(self, scope_context)
        if(left_type!="int" or right_type!="int"):
            self.error_handler.add_error(f"Cannont apply {multiplicative_expression.type} operator to expressions of type diffrent than int")
        return "int"

    def visit_not_expression(self,not_expression:not_expression, scope_context:validator_context):
        negated_type=not_expression.left.accept_validator(self,scope_context)
        if(not_expression.is_negated and negated_type!="bool"):
            self.error_handler.add_error(message=f"Not operator can only be applied to the bool type")
        if(not_expression.is_negated):
            return "bool"
        return negated_type
    def visit_property_call_expression(self,variable_expression:property_call_expression, scope_context:validator_context):
        if(variable_expression.name not in scope_context.defined_variables.keys):
            self.error_handler.add_error(f"Undefined variable {variable_expression.name}")

        object_variable=scope_context.defined_variables[variable_expression.name]
        if(object_variable is None):
            return ""
        
        if(object_variable.type not in self.defined_classes.keys()):
            self.error_handler.add_error(f"Variable {object_variable.name} does not support . operator")
            return ""
        if(not object_variable.is_initialized):
            self.error_handler.add_error(f"Variable {object_variable.name} is not initialized")

        variable_class=self.defined_classes[object_variable.type]
        if(variable_expression.property_name not in variable_class.defined_properties.keys()):
            self.error_handler.add_error(f"Class {object_variable.type} does not have property {variable_expression.property_name}")
        property_dec=variable_class.defined_properties[variable_expression.property_name]
        if(property_dec is None):
            return ""
        return property_dec.type
        
    def visit_variable_expression(self,variable_expression:variable_expression, scope_context:validator_context):
        if(variable_expression.name not in scope_context.defined_variables.keys()):
            self.error_handler.add_error(f"Variable {variable_expression.name} is undefined")
        variable=scope_context.defined_variables[variable_expression.name]
        type=variable.type
        if(variable is None):
            return ""
        if(not variable.is_initialized):
            self.error_handler.add_error(f"Variable {variable_expression.name} is uninitialized")
        return type

    def visit_method_call_expression(self,method_call_expression: method_call_expression, scope_context:validator_context):
        self.validate_method_call(method_call_expression, scope_context)
        variable_type=scope_context.defined_variables[method_call_expression.object_name].type
        return self.defined_classes[variable_type].functions[method_call_expression.function.name].type

    def visit_function_call_expression(self,function_call_expression: function_call_expression, scope_context:validator_context):
        self.validate_function_call(function_call_expression, scope_context)
        if(function_call_expression.name in self.defined_classes.keys()):
            return self.defined_classes[function_call_expression.name].name
        return scope_context.defined_functions[function_call_expression.name].type

    def visit_int_literal_expression(self,int_literal_expression: int_literal_expression, scope_context:validator_context):
        return "int"

    def visit_bool_literal_expression(self,bool_literal_expression: bool_literal_expression, scope_context:validator_context):
        return "bool"

    def visit_string_literal_expression(self,string_literal_expression:string_literal_expression, scope_context:validator_context):
        return "string"
#endregion


    def validate_function_call(self,function_call, scope_context:validator_context):
        if(function_call.name not in self.defined_functions.keys() and function_call.name not in self.defined_classes.keys() and function_call.name not in std.std_functions.keys()):
            self.error_handler.add_error(f"Call undefined function {function_call.name}")
            return False
        
        called_function: function_definition=None
        if(function_call.name in self.defined_classes.keys()):
            called_function=self.defined_classes[function_call.name].constructor
        elif(function_call.name in scope_context.defined_functions.keys()):
            called_function=scope_context.defined_functions[function_call.name]
        elif(function_call.name in std.std_functions.keys()):
            called_function=std.std_functions[function_call.name]
        if(called_function is None):
            raise Exception("Unexpected error in function_call_validation")
        self.validate_call_arguments(function_call, called_function,scope_context)
        return True

    def validate_method_call(self,method_call, scope_context:validator_context):
        if(method_call.object_name not in scope_context.defined_variables.keys()):
            self.error_handler.add_error(f"Use of undefined variable {method_call.object_name}")
            return False
        
        object_variable=scope_context.defined_variables[method_call.object_name]
        if(object_variable.type not in self.defined_classes.keys()):
            self.error_handler.add_error(f"Variable {object_variable.name} does not support . operator")
            return False
        if(not object_variable.is_initialized):
            self.error_handler.add_error(f"Variable {object_variable.name} is not initialized")
        
        object_class=self.defined_classes[object_variable.type]
        if(method_call.function.name not in object_class.functions.keys()):
            self.error_handler.add_error(f"Call undefined method {method_call.function.name} on object {object_variable.name}")
            return False

        self.validate_call_arguments(method_call.function, self.defined_classes[object_variable.type].functions[method_call.function.name],scope_context, True)
        return True

    def validate_call_arguments(self,function_call: function_call_instruction, function_definition:function_definition, scope_context:validator_context,is_method=False):
        parameters=function_definition.parameters
        arguments=function_call.arguments
        
        for i in range(0,len(parameters)):
            parameter_type=parameters[i].type
            argument_type=arguments[i].accept_validator(self,scope_context)
            if(parameter_type!=argument_type):
                self.error_handler.add_error(f"Argument type {argument_type} is not assignable to parameter type {parameter_type} in {function_call.name}")

    def validate_class_definition(self,defined_class: defined_class):
        self.validate_instructions_block(defined_class.constructor.instructions,validator_context(defined_class.validator_context))

        for method in defined_class.defined_methods.values():
            self.current_function_type=method.type
            context=validator_context(method.validator_context)
            self.validate_instructions_block(method.instructions, context)