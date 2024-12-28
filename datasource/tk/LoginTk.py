from tkinter import StringVar
from PIL import Image, ImageTk

class LoginTk:

    def __init__(self):
        self.username = StringVar()
        self.password = StringVar()
        self.img_hide = None
        self.img_show = None
        self.load_image()

    def load_image(self):
        self.show = Image.open("./images/eye.png")
        self.img_show = ImageTk.PhotoImage(self.show)
        self.hide = Image.open("./images/hide.png")
        self.img_hide = ImageTk.PhotoImage(self.hide)
