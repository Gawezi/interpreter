

class validator_context:
    def __init__(self, validator_context):
        self.defined_functions=validator_context.defined_functions
        self.defined_variables=validator_context.defined_variables

    def __init__(self, defined_functions, defined_variables):
        self.defined_functions=defined_functions
        self.defined_variables=defined_variables

    def __init__(self):
        self.defined_functions={}
        self.defined_variables={}