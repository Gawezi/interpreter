from email import parser
from LexerModule.lexer import Lexer
from LexerModule.token import Token
from interpreter import interpreter
from tkinter import filedialog
from error_handler import error_handler
from LexerModule.lexer import Lexer
from ParserModule.parser_instance import Parser
from ValidatorModule.validator import validator
from ExecutorModule.executor import executor
from source_reader import file_reader


def main():
    file=filedialog.askopenfilename()
    error=error_handler()
    lexer=Lexer(file_reader(file),error)
    # token=None
    # while((token:=lexer.get_next_token()).type!=Token.Type.EndOfFile):
    #     print(token.value)
    pars=Parser(lexer,error)
    program=pars.parse_program()
    print("sparsowałem")


main()
