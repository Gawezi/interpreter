
def create_copy_of_dict(dict):
    return {key: value for key,value in dict.items()}
class validator_context:
    def __init__(self, validator_context=None):
        if(validator_context is not None):
            self.defined_functions=create_copy_of_dict(validator_context.defined_functions)
            self.defined_variables=create_copy_of_dict(validator_context.defined_variables)
        else:
            self.defined_functions={}
            self.defined_variables={}

