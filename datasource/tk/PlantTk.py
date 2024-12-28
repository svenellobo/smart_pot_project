from tkinter import StringVar, IntVar, BooleanVar, DoubleVar



class PlantTk:

    def __init__(self):

        self.name = StringVar()
        self.plant_image = StringVar()
        self.plant_ph_high = DoubleVar()
        self.plant_ph_low = DoubleVar()
        self.sunlight_high = IntVar()
        self.sunlight_low = IntVar()
        self.temperature_high = IntVar()
        self.temperature_low = IntVar()
        self.watering = IntVar()
        self.plant_info = StringVar()
        self.plant_web = StringVar()
