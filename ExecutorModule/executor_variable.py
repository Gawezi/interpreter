
class exe_variable:
    def __init__(self, name, type, value, properties):
        self.name=name
        self.type=type
        self.value=value
        self.properties=properties

    def __init__(self, exe_variable):
        self.name=exe_variable.name
        self.type=exe_variable.type
        self.value=exe_variable.value
        self.properties=exe_variable.properties
