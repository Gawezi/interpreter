def create_copy_of_dict(dict):
    return {key: value for key,value in dict.items()}
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
        self.properties=create_copy_of_dict(exe_variable.properties)

    def __init__(self):
        self.name=""
        self.type=""
        self.value=""
        self.properties={}
