import tkinter as tk
from screens.LoginScreen import LoginScreen
import sqlite3



class App(tk.Tk):

    DB_NAME = "PyFlora.db"


    def __init__(self, title, geo):
        super().__init__()
        self.db = sqlite3.connect(self.DB_NAME)
        self.title(title)
        #self.width = self.winfo_screenwidth()
        #self.height = self.winfo_screenheight()
        #self.geometry("%dx%d" % (self.width, self.height))
        self.geometry(geo)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.create_screen()



    def create_screen(self):
        LoginScreen(self, self.db)

if __name__ == '__main__':
    app = App("Py Flora Posuda", "1400x800")
    app.mainloop()

