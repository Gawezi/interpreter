from enum import Enum

class Token:

    class Type(Enum):
        Program="program"
        Class="class"
        Def="def"
        Int="int"
        Bool="bool"
        False_="false"
        True_="true"
        Void="void"
        If="if"
        Else="else"
        While="while"
        Return="return"

        RoundOpenBracket="("
        RoundCloseBracket=")"
        CurlyOpenBracket="{"
        CurlyCloseBracket="}"

        Plus="+"
        Minus="-"
        Multiplication="*"
        Division="/"
        Modulo="%"

        Less="<"
        Greater=">"
        Equal="=="
        NotEqual="!="
        LessOrEqual="<="
        GreaterOrEqual=">="

        And="and"
        Or="or"
        Not="not"

        IntLiteral="int_literal"
        BoolLiteral="bool_literal"
        StringLiteral="string_literal"

        Identifier="id"
        Assign="="
        Semicolon=";"
        Comma=","
        Dot="."
        Init="init"
        EndOfFile="end_of_file"
        Invalid="invalid"


    def __init__(self,type, value=None, line=-1,position=-1):
        self.type=type
        self.value=value
        self.line=line
        self.position=position
