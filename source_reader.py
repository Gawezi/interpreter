class readerInterface:
    def get_char(self):
        print("that is just an interface")

    def give_char_back(self,char):
        print("that is just an interface")

class stream_reader(readerInterface):
    text=""
    def __init__(self):
        super().__init__()
        text=""
        while(True):
            inp=input()
            if(inp==""):
                break
            text+=inp+"\n"
        self.text=text

    def giveChar(self):
        if(self.text==""):
            return ""
        ch=self.text[0]
        self.text=self.text[1:]
        return ch

    def getCharBack(self,char):
        self.text=char+self.text

class file_reader(readerInterface):

    text=""
    def __init__(self,filename):
        super().__init__()
        self.text=open(filename).read()
        #text=text[text.find("PROGRAM"):]

    def get_char(self):
        if(self.text==""):
            return ""
        ch=self.text[0]
        self.text=self.text[1:]
        return ch

    def give_char_back(self,char):
        self.text=char+self.text


class text_reader(readerInterface):

    text=""
    def __init__(self,Text):
        super().__init__()
        self.text=Text

    def giveChar(self):
        if(self.text==""):
            return ""
        ch=self.text[0]
        self.text=self.text[1:]
        return ch

    def getCharBack(self,char):
        self.text=char+self.text


class OneCharFileReader(readerInterface):

    file=""
    text=""
    def __init__(self,filename):
        super().__init__()
        self.file=open(filename,'r')
        #text=text[text.find("PROGRAM"):]

    def giveChar(self):
        if(self.text!=""):
            return self.text[0]
        ch=self.file.read(1)
        return ch

    def getCharBack(self,char):
        self.text=char+self.text