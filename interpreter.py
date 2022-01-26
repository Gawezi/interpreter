from error_handler import error_handler
from LexerModule.lexer import Lexer
from ParserModule.parser import Parser
from ValidatorModule.validator import validator
from ExecutorModule.executor import executor
from source_reader import file_reader
class interpreter:
    def interpret_program(self, file):

        try:
            err_handler = error_handler()
            lexer=Lexer(file_reader(file), err_handler)
            parser=Parser(lexer, err_handler)
            program = parser.parse_program()
            sem_validator= validator(err_handler)
            valid_program= sem_validator.validate_program(program)
            execut=executor()
            execut.execute_program(valid_program)
            return True

        except:
            return False