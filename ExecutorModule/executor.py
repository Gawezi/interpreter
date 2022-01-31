from ast import arguments
from ExecutorModule.executor_context import executor_context
from ExecutorModule.executor_variable import exe_variable
from ParserModule.expressions import additive_expression, and_expression, bool_literal_expression, function_call_expression, int_literal_expression, method_call_expression, multiplicative_expression, not_expression, or_expression, property_call_expression, relative_expression, string_literal_expression, variable_expression
from ParserModule.instructions import assignment_instruction, function_call_instruction, if_else_instruction, method_call_instruction, return_instruction, variable_declaration_instruction, while_instruction
from ValidatorModule.validator import IVisitor
from ValidatorModule.valid_objects import *
from custom_exception import ReturnException
from std import *
class executor(IVisitor):
    def __init__(self):
        super().__init__()
        self.variable_to_return=None    

    def execute_program(self,program:valid_program):
        main_function=program.valid_functions["main"]
        context=executor_context()
        context.functions=program.valid_functions
        context.classes=program.valid_classes
        context.variables={}
        self.execute_function(main_function, context)

    def execute_function(self, function_definition:function_definition, scope_context:executor_context):
        try:
            if(function_definition.name=="Change"):
                print("kupa")
            if(function_definition.name in std_functions):
                print(str(next(iter(scope_context.variables.values())).value))
            if(function_definition.name in scope_context.classes.keys()):
                self.execute_instructions_block(function_definition.instructions, scope_context)
                v=exe_variable()
                v.type=function_definition.name
                v.properties=scope_context.variables
                
                return v
            self.execute_instructions_block(function_definition.instructions, scope_context)

        except ReturnException:
            return exe_variable(self.variable_to_return)


    def execute_instructions_block(self,instructions, scope_context:executor_context):
        for i in instructions:
            i.accept_executor(self,scope_context)


#region INSTRUCTION_VISITORS
    def visit_var_declaration_instruction(self,variable_declaration:variable_declaration_instruction, scope_context:executor_context):
        var=None
        if(variable_declaration.expression is not None):
            var=variable_declaration.expression.accept_executor(self,scope_context)
        if(var is None):
            var=exe_variable()
            var.type=variable_declaration.type
            var.name=variable_declaration.name
        var.type=variable_declaration.type
        var.name=variable_declaration.name
        scope_context.variables[var.name]=var

    def visit_assignment_instruction(self,assignment:assignment_instruction, scope_context:executor_context):
        new_val=assignment.expression.accept_executor(self, scope_context)
        new_val.name=assignment.variable_name
        scope_context.variables[assignment.variable_name]=new_val

    def visit_function_call_instruction(self,function_call:function_call_instruction, scope_context:executor_context):
        function=None
        if(function_call.name in std_functions.keys()):
            function=std_functions[function_call.name]
        else:
            function=scope_context.functions[function_call.name]
        
        function_context=self.execute_call_arguments(function_call, function,scope_context)
        function_context.classes=scope_context.classes
        function_context.functions=scope_context.functions
        self.execute_function(function, function_context)

    def visit_method_call_instruction(self,method_call:method_call_instruction, scope_context:executor_context):
        method=scope_context.classes[scope_context.variables[method_call.object_name].type].methods[method_call.function.name]
        method_context=self.execute_call_arguments(method_call.function, method,scope_context)
        method_context.classes=scope_context.classes
        method_context.functions=scope_context.classes[scope_context.variables[method_call.object_name].type].methods
        for key in scope_context.variables[method_call.object_name].properties.keys():
            method_context.variables[key]=scope_context.variables[method_call.object_name].properties[key]
        self.execute_function(method,method_context)
        for key in scope_context.variables[method_call.object_name].properties.keys():
            scope_context.variables[method_call.object_name].properties[key]=method_context.variables[key].value



    def visit_return_instruction(self,return_instruction:return_instruction, scope_context:executor_context):
        expression_type=None
        if(return_instruction.expression is not None):
            self.variable_to_return=return_instruction.expression.accept_executor(self,scope_context)
            raise ReturnException()
        self.variable_to_return=None
        raise ReturnException()

    def visit_if_else_instruction(self,if_else_instruction:if_else_instruction, scope_context:executor_context):
        base_vars_names=scope_context.variables.keys()
        condition_val=if_else_instruction.condition.accept_executor(self,scope_context)
        actual_val=True
        if(condition_val.value=="false"):
            actual_val=False
        if(actual_val):
            self.execute_instructions_block(if_else_instruction.if_instructions,scope_context)
        else:
            if(if_else_instruction.else_instructions is not None):
                self.execute_instructions_block(if_else_instruction.else_instructions,scope_context)
        
        var_names_to_delete=[]
        for key in scope_context.variables.keys():
            if(key not in base_vars_names):
                var_names_to_delete.append(key)
        for name in var_names_to_delete:
            scope_context.variables.pop(name)
        

    def visit_while_instruction(self,while_instruction:while_instruction, scope_context:executor_context):
        base_vars_names=scope_context.variables.keys()
        condition_val=while_instruction.condition.accept_executor(self,scope_context)
        actual_val=True
        if(condition_val.value=="false"):
            actual_val=False
        while(actual_val):
            self.execute_instructions_block(while_instruction.instructions,scope_context)
            condition_val=while_instruction.condition.accept_executor(self,scope_context)
            if(condition_val.value=="false"):
                actual_val=False
            if(condition_val.value=="true"):
                actual_val=True
        
        var_names_to_delete=[]
        for key in scope_context.variables.keys():
            if(key not in base_vars_names):
                var_names_to_delete.append(key)
        for name in var_names_to_delete:
            scope_context.variables.pop(name)
#endregion

#region EXPRESSION_VISITOR
    def visit_or_expression(self,or_expression:or_expression, scope_context:executor_context):
        left_value=or_expression.left.accept_executor(self,scope_context)
        if(bool(left_value.value)):
            exe_var=exe_variable()
            exe_var.type="bool"
            exe_var.value="true"
            return exe_var
        
        right_value=or_expression.right.accept_executor(self,scope_context)
        exe_var=exe_variable()
        exe_var.type="bool"
        exe_var.value=right_value.value
        return exe_var
        

    def visit_and_expression(self,and_expression:and_expression, scope_context:executor_context):
        left_value=and_expression.left.accept_executor(self,scope_context)
        if(not bool(left_value.value)):
            exe_var=exe_variable()
            exe_var.type="bool"
            exe_var.value="false"
            return exe_var
        
        right_value=and_expression.right.accept_executor(self,scope_context)
        exe_var=exe_variable()
        exe_var.type="bool"
        exe_var.value=right_value.value
        return exe_var



    def visit_relative_expression(self,relative_expression:relative_expression, scope_context:executor_context):
        left_value=relative_expression.left.accept_executor(self,scope_context)
        right_value=relative_expression.right.accept_executor(self,scope_context)
        value=False

        if(left_value.type=="bool"):
            actual_left_value=bool(left_value.value)
            actual_right_value=bool(right_value.value)
            if(relative_expression.type=="=="):
                value=actual_left_value==actual_right_value
            else:
                value=actual_left_value!=actual_right_value
        else:
            actual_left_int_val=int(left_value.value)
            actual_right_int_val=int(right_value.value)
            relation=relative_expression.type
            if(relation=="=="):
                value=actual_left_int_val==actual_right_int_val
            elif(relation=="!="):
                value=actual_left_int_val!=actual_right_int_val
            elif(relation=="<"):
                value=actual_left_int_val<actual_right_int_val
            elif(relation=="<="):
                value=actual_left_int_val<=actual_right_int_val
            elif(relation==">"):
                value=actual_left_int_val>actual_right_int_val
            elif(relation==">="):
                value=actual_left_int_val>=actual_right_int_val
            else:
                raise Exception("Wrong relative type")
        
        exe_var=exe_variable()
        exe_var.type="bool"
        if(value):
            exe_var.value="true"
        else:
            exe_var.value="false"
        
        return exe_var




    def visit_additive_expression(self,additive_expression:additive_expression, scope_context:executor_context):
        left_val=additive_expression.left.accept_executor(self,scope_context)
        right_val=additive_expression.right.accept_executor(self,scope_context)
        actual_left_val=int(left_val.value)
        actual_right_val=int(right_val.value)
        value=0
        if(additive_expression.type=="+"):
            value=actual_left_val+actual_right_val
        elif(additive_expression.type=="-"):
            value=actual_left_val-actual_right_val
        else:
            raise Exception("wrong type of additive expression")
        exe=exe_variable()
        exe.type="int"
        exe.value=str(value)
        exe.name=left_val.name
        return exe



    def visit_multiplicative_expression(self,multiplicative_expression: multiplicative_expression, scope_context:executor_context):
        left_val=multiplicative_expression.left.accept_executor(self,scope_context)
        right_val=multiplicative_expression.right.accept_executor(self,scope_context)
        actual_left_val=int(left_val.value)
        actual_right_val=int(right_val.value)
        value=0
        if(multiplicative_expression.type=="*"):
            value=actual_left_val*actual_right_val
        elif(multiplicative_expression.type=="%"):
            value=actual_left_val%actual_right_val
        elif(multiplicative_expression.type=="/"):
            if(actual_right_val==0):
                raise Exception("cannot divide by zero")
            value=int(actual_left_val/actual_right_val)
        else:
            raise Exception("wrong type of additive expression")
        exe=exe_variable()
        exe.type="int"
        exe.value=str(value)
        exe.name=left_val.name
        return exe


    def visit_not_expression(self,not_expression: not_expression, scope_context:executor_context):
        val=not_expression.left.accept_executor(self,scope_context)
        actual_value=bool(val.value)
        exe=exe_variable()
        exe.type="bool"
        exe.value==str(not actual_value)
        return exe

    def visit_variable_expression(self,variable_expression:variable_expression, scope_context:executor_context):
        variable=scope_context.variables[variable_expression.name] 
        return exe_variable(exe_variable=variable)

    def visit_property_call_expression(self,property_call_expression:property_call_expression, scope_context:executor_context):
        variable=scope_context.variables[property_call_expression.object_name].properties[property_call_expression.property_name]
        return exe_variable(exe_variable=variable)

    def visit_method_call_expression(self,method_call_expression:method_call_expression, scope_context:executor_context):
        method=scope_context.classes[scope_context.variables[method_call_expression.object_name].type].methods[method_call_expression.function.name]
        method_context=self.execute_call_arguments(method_call_expression.function, method, scope_context)
        method_context.classes=scope_context.classes
        method_context.functions=scope_context.classes[scope_context.variables[method_call_expression.object_name].type].methods
        for key in scope_context.variables[method_call_expression.object_name].properties:
            method_context.variables[key]=scope_context.variables[method_call_expression.object_name].properties[key]
        return self.execute_function(method,method_context)


    def visit_function_call_expression(self,function_call_expression:function_call_expression, scope_context:executor_context):
        function=None
        if((function:=scope_context.functions.get(function_call_expression.name))is not None):
            function_context=self.execute_call_arguments(function_call_expression,function,scope_context)
            function_context.classes=scope_context.classes
            function_context.functions=scope_context.functions
            return self.execute_function(function,function_context)
        
        constructor=scope_context.classes[function_call_expression.name].constructor
        constructor_context=self.execute_call_arguments(function_call_expression, constructor,scope_context)
        constructor_context.classes=scope_context.classes
        constructor_context.functions=scope_context.classes[function_call_expression.name].methods
        new_object=self.execute_function(constructor,constructor_context)
        to_delete=[]
        for key in new_object.properties.keys():
            if(key not in scope_context.classes[function_call_expression.name].properties.keys()):
                to_delete.append(key)
        for v in to_delete:
            new_object.properties.pop(v)
        return new_object

    def visit_int_literal_expression(self,int_literal_expression:int_literal_expression, scope_context:executor_context):
        variable=exe_variable()
        variable.type="int"
        variable.value=str(int_literal_expression.value)
        return variable

    def visit_bool_literal_expression(self,bool_literal_expression:bool_literal_expression, scope_context:executor_context):
        variable=exe_variable()
        variable.type="bool"
        variable.value=str(bool_literal_expression.value)
        return variable

    def visit_string_literal_expression(self,string_literal_expression:string_literal_expression, scope_context:executor_context):
        variable=exe_variable()
        variable.type="string"
        variable.value=string_literal_expression.value
        return variable

#endregion

    def execute_call_arguments(self,function_call, function_definition:function_definition, scope_context: executor_context):
        parameters=function_definition.parameters
        arguments=function_call.arguments

        context=executor_context()
        for i in range(0,len(arguments)):
            argument_val=arguments[i].accept_executor(self, scope_context)
            parameter=parameters[i]
            argument_val.type=parameter.type
            argument_val.name=parameter.name
            context.variables[argument_val.name]=argument_val
        
        return context

