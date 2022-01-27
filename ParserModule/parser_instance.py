from ParserModule.definitions import *
from ParserModule.expressions import *
from ParserModule.instructions import *
from LexerModule.token import Token
from LexerModule.lexer import Lexer
from error_handler import error_handler


class program_instance:
    def __init__(self, functions, classes):
        self.functions=functions
        self.classes=classes


class Parser:
    def __init__(self, lexer: Lexer, error_handler:error_handler):
        self.lexer=lexer
        self.error_handler=error_handler
        self.functions=[]
        self.classes=[]
        self.error_happened=False


        
    def parse_program(self):

        self.must_be_with_exception(Token.Type.Program)
        self.must_be_with_exception(Token.Type.CurlyOpenBracket)
        functions=[]
        classes=[]
        definition=None
        while ((definition:=self.try_parse_class()) is not None ) or ((definition:=self.try_parse_function()) is not None):
            if(type(definition) is class_definition):
                classes.append(definition)
            if(type(definition) is function_definition):
                functions.append(definition)
        self.must_be_with_exception(Token.Type.CurlyCloseBracket)
        if(not self.error_happened):
            return program_instance(functions, classes)
        else:
            self.error_handler.stop_everything()
            return None

    def try_parse_class(self):
        if(not self.may_be(Token.Type.Class)):
            return None
        self.must_be_with_exception(Token.Type.Identifier)
        name=self.lexer.current_token.value

        self.must_be_with_exception(Token.Type.CurlyOpenBracket)
        self.must_be_with_exception(Token.Type.Def)
        self.must_be_with_exception(Token.Type.Init)
        constructor_parameters=self.parse_parameters()

        constructor_instructions=self.parse_instructions()

        properties={}
        proper=None
        while((proper:=self.try_parse_property())is not None):
            properties[proper.name]=proper

        functions={}
        func=None
        while((func:=self.try_parse_function())is not None):
            functions[func.name]=func

        self.must_be_with_exception(Token.Type.CurlyCloseBracket)

        constructor=function_definition(name, name, constructor_parameters, constructor_instructions)
        return class_definition(name,constructor, functions, properties)

    def try_parse_function(self):
        if( not self.may_be(Token.Type.Def)):
            return None 

        self.must_be_list([Token.Type.Int, Token.Type.Void,Token.Type.Bool,Token.Type.Identifier])
        type=self.lexer.current_token.type.value

        self.must_be_with_exception(Token.Type.Identifier)
        name=self.lexer.current_token.value
        
        parameters=self.parse_parameters()


        instructions=self.parse_instructions()


        return function_definition(name,type,parameters,instructions)

    def parse_parameters(self):
        self.must_be_with_exception(Token.Type.RoundOpenBracket)
        parameters=[]
        if(not self.may_be_with_list([Token.Type.Int, Token.Type.Bool, Token.Type.Identifier])):
            self.must_be_with_exception(Token.Type.RoundCloseBracket)
            return parameters

        type=self.lexer.current_token.type.value
        self.must_be_with_exception(Token.Type.Identifier)
        name=self.lexer.current_token.value
        parameters.append(parameter(name,type))

        while(self.may_be(Token.Type.Comma)):
            self.must_be_list([Token.Type.Int, Token.Type.Void,Token.Type.Bool,Token.Type.Identifier])
            type=self.lexer.current_token.type.value
            self.must_be_with_exception(Token.Type.Identifier)
            name=self.lexer.current_token.value

            for param in parameters:
                if param.name==name:
                    self.error_handler.handle_fatal_error("Invalid name: line"+self.lexer.current_token.line+". Parameter with name "+str(name +" already exists."))
            parameters.append(parameter(name,type))
        self.must_be_with_exception(Token.Type.RoundCloseBracket)
        
        return parameters

        


#region INSTRUCTIONS
    def parse_instructions(self):
        self.must_be_with_exception(Token.Type.CurlyOpenBracket)
        instructions=[] # listy jako jedne z niewielu rzeczy mogą byc nadpisywane w parametrach
        while(self.try_parse_if_instruction(instructions) or self.try_parse_while_instruction(instructions) or self.try_parse_flat_init_instruction(instructions) or self.try_parse_identifier_instruction(instructions) or self.try_parse_return_instruction(instructions)):
            pass
        self.must_be_with_exception(Token.Type.CurlyCloseBracket)
        return instructions

    def try_parse_if_instruction(self,instructions):
        if(not self.may_be(Token.Type.If)):
            return False

        self.must_be_with_exception(Token.Type.RoundOpenBracket)
        condition=self.try_parse_expression()
        if(condition is None):
            self.error_handler.handle_fatal_error("Parsing if condition was not succesfull in line: "+str(self.lexer.current_token.line)+ " ,position: "+str(self.lexer.current_token.position))

        self.must_be_with_exception(Token.Type.RoundCloseBracket)

        if_instructions=self.parse_instructions()
        else_instructions=[]
        if(self.may_be(Token.Type.Else)):
            else_instructions=self.parse_instructions()
        
        instructions.append(if_else_instruction(condition,if_instructions, else_instructions))
        return True
            
    def try_parse_while_instruction(self,instructions):
        if(not self.may_be(Token.Type.While)):
            return False
        self.must_be_with_exception(Token.Type.RoundOpenBracket)

        condition=self.try_parse_expression()
        if(condition is None):
            self.error_handler.handle_fatal_error("Parsing while condition was not succesfull in line: "+str(self.lexer.current_token.line)+ " ,position: "+str(self.lexer.current_token.position))

        self.must_be_with_exception(Token.Type.RoundCloseBracket)

        while_instructions=self.parse_instructions()


        instructions.append(while_instruction(condition, while_instructions))
        return True

    def try_parse_flat_init_instruction(self,instructions):

        if(not self.may_be_with_list([Token.Type.Int, Token.Type.Bool])):
            return False
        type=self.lexer.current_token.type.value
        self.must_be_with_exception(Token.Type.Identifier)
        name=self.lexer.current_token.value
        express=None
        if(self.may_be(Token.Type.Assign)):
            express=self.try_parse_expression()
            if(express is None):
                self.error_handler.handle_fatal_error("Invalid assign expression: line"+str(self.lexer.current_token.line)+". Parameter with name "+str(name) +" already exists.")
        self.must_be_with_exception(Token.Type.Semicolon)
        instructions.append(variable_declaration_instruction(name,type,express))
        return True

    def try_parse_identifier_instruction(self,instructions):
        if(not self.may_be(Token.Type.Identifier)):
            return False

        token = self.lexer.current_token
        expres=None
        if(self.may_be(Token.Type.Identifier)):
            name=self.lexer.current_token.value
            if(self.may_be(Token.Type.Assign)):
                expres=self.try_parse_expression()
                if(expres==None):
                    self.error_handler.handle_fatal_error("Invalid assign: line"+str(self.lexer.current_token.line)+". Parameter with name "+str(name) +" already exists.")
            self.must_be_with_exception(Token.Type.Semicolon)
            instructions.append(variable_declaration_instruction(name,token.value,expres))
            return True
        
        if(self.may_be(Token.Type.Assign)):
            expres=self.try_parse_expression()
            if(expres==None):
                    self.error_handler.handle_fatal_error("Invalid assign: line"+str(self.lexer.current_token.line))
            self.must_be_with_exception(Token.Type.Semicolon)
            instructions.append(assignment_instruction(token.value,expres))
            return True
        
        if(self.may_be(Token.Type.RoundOpenBracket)):
            args=self.parse_arguments()
            self.must_be_with_exception(Token.Type.RoundCloseBracket)
            self.must_be_with_exception(Token.Type.Semicolon)
            instructions.append(function_call_instruction(token.value,args))
            return True

        if(self.may_be(Token.Type.Dot)):
            self.must_be_with_exception(Token.Type.Identifier)
            name=self.lexer.current_token.value
            self.must_be_with_exception(Token.Type.RoundOpenBracket)
            args=self.parse_arguments()
            self.must_be_with_exception(Token.Type.RoundCloseBracket)
            self.must_be_with_exception(Token.Type.Semicolon)
            instructions.append(method_call_instruction(token.value,function_call_instruction(name,args)))
            return True
        
        return False


    def try_parse_return_instruction(self,instructions):
        if(not self.may_be(Token.Type.Return)):
            return False

        express=None
        if(not self.may_be(Token.Type.Semicolon)):
            express=self.try_parse_expression()
            if(express is not None):
                self.must_be_with_exception(Token.Type.Semicolon)
        instructions.append(return_instruction(express))
        return True
#endregion

    def parse_arguments(self):
        arguments=[]

        express=None
        while((express:=self.try_parse_expression()) is not None):
            arguments.append(express)
            if(not self.may_be(Token.Type.Comma)):
                break        
        return arguments

#region EXPRESSIONS
    def try_parse_expression(self):
        
        left_express=self.try_parse_and_expression()
        if(left_express is None):
            return None
        
        
        while(self.may_be(Token.Type.Or)):
            right_express=self.try_parse_and_expression()
            if(right_express is None):
                    self.error_handler.handle_fatal_error("Invalid 'and' expression: line"+str(self.lexer.current_token.line))
            left_express=or_expression(left_express,right_express)

        return left_express

    def try_parse_and_expression(self):
        left_express=self.try_parse_relative_expression()
        if(left_express is None):
            return None

        while(self.may_be(Token.Type.And)):
            right_express=self.try_parse_relative_expression()
            if(right_express is None):
                    self.error_handler.handle_fatal_error("Invalid 'relative' expression: line"+str(self.lexer.current_token.line))
            left_express=and_expression(left_express,right_express)

        return left_express

    def try_parse_relative_expression(self):
        left_express=self.try_parse_additive_expression()
        if(left_express is None):
            return None
        
        while(self.may_be_with_list([Token.Type.Less,Token.Type.Greater,Token.Type.LessOrEqual,Token.Type.GreaterOrEqual,Token.Type.NotEqual,Token.Type.Equal])):
            type=self.lexer.current_token.type.value
            right_express=self.try_parse_additive_expression()
            if(right_express is None):
                    self.error_handler.handle_fatal_error("Invalid 'additive' expression: line"+str(self.lexer.current_token.line))
            left_express=relative_expression(left_express,right_express,type)
        return left_express

    def try_parse_additive_expression(self):
        left_express=self.try_parse_multiplicative_expression()
        if(left_express is None):
            return None
        
        #is_additive
        while(self.may_be_with_list([Token.Type.Plus, Token.Type.Minus])):
            type=self.lexer.current_token.type.value
            right_express=self.try_parse_multiplicative_expression()
            if(right_express is None):
                    self.error_handler.handle_fatal_error("Invalid 'multiply' expression: line"+str(self.lexer.current_token.line))
            left_express=additive_expression(left_express,right_express,type)
        return left_express

    def try_parse_multiplicative_expression(self):
        left_express=self.try_parse_negation_expression()
        if(left_express is None):
            return None
        
        #is_multiply
        while(self.may_be_with_list([Token.Type.Multiplication, Token.Type.Division,Token.Type.Modulo])):
            type=self.lexer.current_token.type.value
            right_express=self.try_parse_negation_expression()
            if(right_express is None):
                    self.error_handler.handle_fatal_error("Invalid 'negation' expression: line"+str(self.lexer.current_token.line))
            left_express=multiplicative_expression(left_express,right_express,type)
        return left_express

    def try_parse_negation_expression(self):
        is_negated=self.may_be(Token.Type.Not)
        factor=None
        if(((factor:=self.try_parse_literal()) is not None) or ((factor:=self.try_parse_bracket_expression()) is not None) or ((factor:=self.try_parse_identifier_expression()) is not None)):
            return factor
        if(is_negated):
            return not_expression(factor, is_negated)


    def try_parse_bracket_expression(self):
        
        if(not self.may_be(Token.Type.RoundOpenBracket)):
            return None
        
        express=self.try_parse_expression()
        if(express is None):
            self.error_handler.handle_fatal_error("Invalid 'bracket' expression: line"+str(self.lexer.current_token.line))
        self.must_be_with_exception(Token.Type.RoundCloseBracket)
        return express


    def try_parse_identifier_expression(self):
        if(not self.may_be(Token.Type.Identifier)):
            return None
        
        token = self.lexer.current_token
        if(self.may_be(Token.Type.RoundOpenBracket)):
            args = self.parse_arguments()
            self.must_be_with_exception(Token.Type.RoundCloseBracket)
            expres=function_call_expression(token.value,args)
            return expres

        if(self.may_be(Token.Type.Dot)):
            self.must_be_with_exception(Token.Type.Identifier)
            name=self.lexer.current_token.value
            if(not self.may_be(Token.Type.RoundOpenBracket)):
                expres=property_call_expression(token.value,name)
                return expres
            args=self.parse_arguments()
            self.must_be_with_exception(Token.Type.RoundCloseBracket)
            expres=method_call_expression(token.value, function_call_expression(name,args))
            return expres
        
        expres=variable_expression(token.value)
        return expres
#endregion

#region LITERAL
    def try_parse_literal(self):

        express=self.try_parse_int_literal()
        if(express is not None):
            return express

        express=self.try_parse_bool_literal()
        if(express is not None):
            return express

        express=self.try_parse_string_literal()
        if(express is not None):
            return express

        return None

    def try_parse_int_literal(self):
        minus=self.may_be(Token.Type.Minus)
        number=self.may_be(Token.Type.IntLiteral)
        if(minus and not number):
            self.error_handler.handle_fatal_error("Invalid 'minus' before string or bool: line"+str(self.lexer.current_token.line))
        if(not number):
            return None
        
        return int_literal_expression(int(self.lexer.current_token.value))

    def try_parse_bool_literal(self):
        if(self.may_be(Token.Type.False_)):
            return bool_literal_expression(False)
        
        if(self.may_be(Token.Type.True_)):
            return bool_literal_expression(True)

        return None

    def try_parse_string_literal(self):
        if(self.may_be(Token.Type.StringLiteral)):
            return string_literal_expression(self.lexer.current_token.value)

        return None
#endregion

        


    def try_parse_property(self):
        if(not self.may_be_with_list([Token.Type.Int,Token.Type.Bool,Token.Type.Identifier])):
            return None

        type=self.lexer.current_token.type.value
        self.must_be_with_exception(Token.Type.Identifier)
        name=self.lexer.current_token.value

        if(not self.may_be(Token.Type.Assign)):
            self.must_be_with_exception(Token.Type.Semicolon)
            property=variable_declaration_instruction(name,type,None)
            return property
        
        literal=self.try_parse_int_literal()
        if(literal is None):
            literal=self.try_parse_bool_literal()
        if(literal is None):
            self.error_handler.handle_fatal_error("Property of type: "+str(type)+ " cannot be initialized. Line: "+str(self.lexer.current_token.line)+" ,position: "+str(self.lexer.current_token.position))
    
        self.must_be_with_exception(Token.Type.Semicolon)
        return variable_declaration_instruction(name,type,literal)
            


#region CHECKERS
    def may_be(self,token_type):
        token=self.lexer.get_next_token()
        if(token.type==token_type):
            return True
        self.lexer.give_token_back(token)
        return False

    def may_be_with_list(self,token_types:list[Token.Type]):
        token=self.lexer.get_next_token()
        for type in token_types:
            if(token.type==type):
                return True
        self.lexer.give_token_back(token)
        return False

    def must_be_list(self, token_types):
        token=self.lexer.get_next_token()
        flag=False
        for type in token_types:
            if(type==token.type):
                flag=True
                break
        if(not flag):
            self.error_handler.handle_fatal_error("Invalid token type in line: "+str((token.line)) + " , position: "+str(token.position))   


    def must_be_with_exception(self,token_type):
        token=self.lexer.get_next_token()
        if(token.type!=token_type):
            self.error_handler.handle_fatal_error("Invalid token type in line: "+str((token.line)) + " , position: "+str(token.position))

#endregion