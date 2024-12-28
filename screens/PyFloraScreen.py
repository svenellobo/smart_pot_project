from tkinter import ttk
import tkinter as tk
from utils.ComponentUtil import ComponentUtil as cu
from screens.PotsScreen import PotScreen
from screens.PlantsScreen import PlantScreen
from screens.UserProfileScreen import UserProfileScreen



class PyFloraScreen(ttk.Frame):

    def __init__(self, parent, db, user_tk):
        super().__init__(parent)
        self.parent = parent
        self.user_tk = user_tk
        self['relief'] = tk.RIDGE
        self['borderwidth'] = 5
        self.db = db
        self.grid()
        self.init_screen()



    def init_screen(self):

        navigation_area = ttk.LabelFrame(self, text="Navigation")
        cu.place_component(navigation_area, 0, 0)

        navigation_area.lift()

        self.btn_pots = ttk.Button(navigation_area, text="PyFlora Pots", command=self.pots_screen)
        cu.place_component(self.btn_pots, 0, 0)

        self.btn_plants = ttk.Button(navigation_area, text="Plants", command=self.plants_screen)
        cu.place_component(self.btn_plants, 0, 1)

        self.btn_user = ttk.Button(navigation_area, text="My Profile", command=lambda: self.user_screen(self.user_tk))
        cu.place_component(self.btn_user, 0, 2)




    def pots_screen(self):
        PotScreen(self.parent, self.db)
        self.grid(padx=10, pady=20, sticky=tk.N)


    def plants_screen(self):
        PlantScreen(self.parent, self.db)
        self.grid(padx=10, pady=20, sticky=tk.N)

    def user_screen(self, user_tk):
        UserProfileScreen(self.parent, self.db, user_tk)
        self.grid(padx=10, pady=20, sticky=tk.N)





