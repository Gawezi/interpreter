import custom_exception as ce

class error_handler:
    def __init__(self):
        self.error_messages=[]
        self.warning_messages=[]

    def add_error(self,message):
        self.error_messages.append(message)
        

    def add_warning(self,message):
        self.warning_messages.append(message)
        
    def print_errors_and_warnings(self):
        print("Errors:")
        for error in self.error_messages:
            print(error)

        print("Warnings:")
        for warning in self.warning_messages:
            print(warning)

    def stop_everything(self):
        self.print_errors_and_warnings()
        raise ce.StopException()

    def handle_fatal_error(self, message):
        self.print_errors_and_warnings()
        print("Fatal error: "+message)
        raise Exception(message)