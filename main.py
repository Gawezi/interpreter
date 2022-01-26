from interpreter import interpreter
from tkinter import filedialog

def main():
    file=filedialog.askopenfilename()
    interpret=interpreter()
    interpret.interpret_program(file)


main()
