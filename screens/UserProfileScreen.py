from tkinter import ttk, messagebox
import tkinter as tk
from utils.ComponentUtil import ComponentUtil as cu
from screens.components.CustomEntry import CustomEntry
from repository.UserRepository import UserRepository
from PIL import Image, ImageTk
from datasource.dto.UserDto import UserDto

class UserProfileScreen(ttk.Frame):

    def __init__(self, parent, db, user_tk):
        super().__init__(parent)
        self.grid(row=0, column=0, padx=30, pady=30)
        self.db = db
        self.parent = parent
        self.repo = UserRepository(self.db)
        self['relief'] = tk.RIDGE
        self['borderwidth'] = 10
        self.pass_visible = False
        self.user_tk = user_tk
        self.init_screen()
        self.load_image()

    def init_screen(self):
        user_info_area = ttk.LabelFrame(self)
        cu.place_component(user_info_area, 0, 0)


        self.name = CustomEntry(user_info_area, 0, 0, "Name", self.user_tk.name)
        self.surname = CustomEntry(user_info_area, 1, 0, "Surname", self.user_tk.surname)
        self.username = CustomEntry(user_info_area, 2, 0, "Username", self.user_tk.username)
        self.password = CustomEntry(user_info_area, 3, 0, "Password", self.user_tk.password, True)

        self.btn_show_password = ttk.Button(user_info_area, image=self.user_tk.img_hide, command=self.toggle_pass_visibility)
        cu.place_component(self.btn_show_password, 3, 1)

        self.close_btn = tk.Button(user_info_area, bg="red", text="X", height=1, width=3, command=self.close)
        self.close_btn.grid(row=0, column=10, pady=5, padx=5, sticky=tk.NW)

        self.update_user_btn = ttk.Button(self, text="Update user", command=self.update_user)
        cu.place_component(self.update_user_btn, 4, 0)

    def close(self):
        self.destroy()
        self.parent.grid()

    def load_image(self):
        self.show = Image.open("./images/eye.png")
        self.img_show = ImageTk.PhotoImage(self.show)
        self.hide = Image.open("./images/hide.png")
        self.img_hide = ImageTk.PhotoImage(self.hide)

    def toggle_pass_visibility(self):
        if not self.pass_visible:
            self.password.entry.config(show="")
            self.btn_show_password.config(image=self.user_tk.img_show)
            self.pass_visible = True

        else:
            self.password.entry.config(show="*")
            self.btn_show_password.config(image=self.user_tk.img_hide)
            self.pass_visible = False

    def update_user(self):
        id = self.user_tk.user_id
        name = self.user_tk.name.get()
        surname = self.user_tk.surname.get()
        user_name = self.user_tk.username.get()
        password = self.user_tk.password.get()
        user: UserDto = UserDto(id, name, surname, user_name, password)
        self.repo.update_user(user)
        self.destroy()
        UserProfileScreen(self.parent, self.db, self.user_tk)
        tk.messagebox.showinfo("User info update", "User information updated successfully.")


