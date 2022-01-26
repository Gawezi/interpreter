from ParserModule.node_interface import Node

class Definition(Node):
    pass

class class_definition(Definition):
    def __init__(self,name,constructor, functions, properties):
        super().__init__()
        self.constructor=constructor
        self.name=name
        self.functions=functions
        self.properties=properties

class function_definition(Definition):
    def __init__(self,name,type, parameters, instructions):
        super().__init__()
        self.type=type
        self.name=name
        self.parameters=parameters
        self.instructions=instructions

class parameter:
    def __init__(self, name,type):
        self.type=type
        self.name=name
