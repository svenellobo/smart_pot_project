from tkinter import StringVar, IntVar, BooleanVar, DoubleVar


class PotTk:

    def __init__(self):

        self.name = StringVar()
        self.ph_value = DoubleVar()
        self.sunlight = IntVar()
        self.water = BooleanVar()
        self.last_watering_date = IntVar()
        self.temperature = IntVar()


