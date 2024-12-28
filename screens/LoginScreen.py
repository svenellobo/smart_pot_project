import tkinter as tk
from tkinter import ttk, messagebox
from utils.ComponentUtil import ComponentUtil as cu
from screens.components.CustomEntry import CustomEntry
from repository.UserRepository import UserRepository
from screens.PyFloraScreen import PyFloraScreen
from datasource.tk.LoginTk import LoginTk
from datasource.tk.UserTk import UserTk


class LoginScreen(ttk.Frame):



    def __init__(self, parent, db):
        super().__init__(parent)
        self.parent = parent
        self.db = db
        self.grid()
        self.repo = UserRepository(self.db)
        self.login_tk = LoginTk()
        self.pass_visible = False
        self.init_screen()


    def init_screen(self):


        self.username = CustomEntry(self, 0, 0, "Username", self.login_tk.username)
        self.password = CustomEntry(self, 1, 0, "Password", self.login_tk.password, True)

        self.btn_show_password = ttk.Button(self, image=self.login_tk.img_hide, command=self.toggle_pass_visibility)
        cu.place_component(self.btn_show_password, 1, 1)

        btn_login = ttk.Button(self, text="Login", command=self.login)
        cu.place_component(btn_login, 2, 0, sticky=tk.EW)



    def login(self):
        if self.login_tk.username.get() != "" and self.login_tk.password.get() != "":
            result = self.repo.fetch_user(self.login_tk.username.get(), self.login_tk.password.get())

            if result is not None:
                user_tk = UserTk()
                user_tk.user_id = result.id
                user_tk.name.set(result.name)
                user_tk.surname.set(result.surname)
                user_tk.username.set(result.username)
                user_tk.password.set(result.password)
                self.grid_remove()
                PyFloraScreen(self.parent, self.db, user_tk)

            else:
                tk.messagebox.showinfo("Login Unsuccessful!", "Wrong username and/or password.")

        else:
            tk.messagebox.showinfo("Login Unsuccessful!", "Please enter username and/or password.")


    def toggle_pass_visibility(self):
        if not self.pass_visible:
            self.password.entry.config(show="")
            self.btn_show_password.config(image=self.login_tk.img_show)
            self.pass_visible = True

        else:
            self.password.entry.config(show="*")
            self.btn_show_password.config(image=self.login_tk.img_hide)
            self.pass_visible = False




