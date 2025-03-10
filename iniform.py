import os
from delphivcl import *

class Form3(Form):

    def __init__(self, owner):
        self.Label1 = None
        self.ListBox1 = None
        self.Button1 = None
        self.LoadProps(os.path.join(os.path.dirname(os.path.abspath(__file__)), "iniform.pydfm"))

    def FormClose(self, Sender, Action):
        pass

def main():
    Application.Initialize()
    Application.Title = 'Arbre Généalogique'
    MainForm = Form3(Application)
    MainForm.Show()
    FreeConsole()
    Application.Run()

if __name__ == '__main__':
    main()
