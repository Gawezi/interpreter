from LexerModule.token import Token
import source_reader as sr


class Lexer:

    def __init__(self, code_reader, error_handler):
        self.code_reader=code_reader
        self.error_handler=error_handler
        self.line=1
        self.position=1
        self.buffored_symbol=""
        self.symbol=""
        self.current_token=None
        self.next_token=None

    def get_next_symbol(self):
        if(self.buffored_symbol):
            symbol=self.buffored_symbol
            self.buffored_symbol=""
            return symbol
        self.position+=1
        return self.code_reader.get_char()
        

    def get_next_token(self):
        if(self.next_token is not None):
            token=self.next_token
            self.next_token=None
            return token
        self.current_token=self.build_next_token()
        return self.current_token

    def give_token_back(self,token):
        self.next_token=token

    def build_next_token(self):
        ch=""
        if((ch:=self.code_reader.get_char())==""):
            return Token(Token.Type.EndOfFile)
        self.code_reader.give_char_back(ch)
        self.position-=1
        
        self.ignore()
        if(self.symbol.isalpha()):
            return self.handle_word()
        
        if(self.symbol.isnumeric()):
            return self.handle_number()
        
        if(self.symbol=='"'):
            return self.handle_string()

        return self.handle_special()

#region HANDLE_THINGS

    def handle_word(self):
        word=self.symbol
        self.symbol=self.get_next_symbol()

        while(self.symbol.isalpha() or self.symbol.isdigit()):
            word+=self.symbol
            self.symbol=self.get_next_symbol()
        
        self.buffored_symbol=self.symbol
        return Token(self.map_string_to_token_type(word), word, self.line, self.position)


    def handle_number(self):
        number=self.symbol
        self.symbol=self.get_next_symbol()

        while(self.symbol.isnumeric()):
            number+=self.symbol
            self.symbol=self.get_next_symbol()

        try:
            n=int(number)
        except Exception:
            self.error_handler.handle_fatal_error("Integer cannot be parsed in line: "+self.line + " , position: "+self.position)

        self.buffored_symbol=self.symbol
        return Token(Token.Type.IntLiteral,number,self.line, self.position)

    def handle_string(self):
        str=""
        self.symbol=self.get_next_symbol()
        while(self.symbol!='"'):
            str+=self.symbol
            self.symbol=self.get_next_symbol()
        return Token(Token.Type.StringLiteral,str, self.line,self.position)

    def handle_special(self):
        first_symbol=self.symbol
        second_symbol=self.get_next_symbol()

        if(second_symbol in signs and first_symbol in signs):
            return Token(self.map_string_to_token_type(first_symbol+second_symbol), first_symbol+second_symbol,self.line, self.position)
        elif(not second_symbol in signs):
            self.code_reader.give_char_back(second_symbol)
            self.position-=1
            return Token(self.map_string_to_token_type(first_symbol),first_symbol,self.line, self.position-1)

            

#endregion

#region IGNORE_THINGS

    def ignore(self):
        self.symbol=self.get_next_symbol()

        while(self.symbol.isspace() or self.symbol=='\n' or self.symbol=='\r' or self.symbol=='#'):
            if(self.symbol=='#'):
                self.handle_comment()
            elif (self.symbol=='\n' or self.symbol=='\r'):
                self.handle_end_of_line()
            else:
                self.handle_space()

    def handle_space(self):
        while(self.symbol.isspace()):
            self.position+=1
            self.symbol=self.get_next_symbol()

    def handle_comment(self):
        while(not (self.symbol=='\n' or self.symbol=='r') ):
            self.symbol=self.get_next_symbol()

    def handle_end_of_line(self):
        self.line+=1
        self.position=0
        self.symbol=self.get_next_symbol()

#endregion    

    def map_string_to_token_type(self, str):
        dict={"program": Token.Type.Program,
        "class": Token.Type.Class,
        "def": Token.Type.Def,
        "int": Token.Type.Int,
        "bool": Token.Type.Bool,
        "false": Token.Type.False_,
        "true": Token.Type.True_,
        "void":Token.Type.Void,
        "if": Token.Type.If,
        "else": Token.Type.Else,
        "while": Token.Type.While,
        "return": Token.Type.Return,
        "(":Token.Type.RoundOpenBracket,
        ")":Token.Type.RoundCloseBracket,
        "{":Token.Type.CurlyOpenBracket,
        "}": Token.Type.CurlyCloseBracket,
        "+":Token.Type.Plus,
        "-":Token.Type.Minus,
        "*":Token.Type.Multiplication,
        "/":Token.Type.Division,
        "%":Token.Type.Modulo,
        "<": Token.Type.Less,
        ">":Token.Type.Greater,
        "==": Token.Type.Equal,
        "!=":Token.Type.NotEqual,
        "<=":Token.Type.LessOrEqual,
        ">=":Token.Type.GreaterOrEqual,

        "and":Token.Type.And,
        "or":Token.Type.Or,
        "not": Token.Type.Not,

        "=":Token.Type.Assign,
        ";":Token.Type.Semicolon,
        ",":Token.Type.Comma,
        ".":Token.Type.Dot,
        "init":Token.Type.Init
        }
        type=dict.get(str)
        if(type is None):
            type=Token.Type.Identifier
        return type


reserved={
        "program",
        "main",
        "return",
        "if",
        "else",
        "or",
        "and",
        "not",
        "true",
        "false",
        "int",
        "bool",
        "print_int",
        "print_bool",
        "print_string"
}

signs={
        "=",
        "<",
        ">",
        "<=",
        ">=",
        "==",
        "!=",
        "+",
        "-",
        "/",
        "!",
        "=",
        "*",
        "%"
}

splitters={
            ",",
            ".",
            ";",
            "{",
            "}",
            "(",
            ")",
}
