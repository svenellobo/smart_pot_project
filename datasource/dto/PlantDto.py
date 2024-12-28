from datasource.tk.PlantTk import PlantTk


class PlantDto:



    def __init__(self, id, name, image, plant_ph_low, plant_ph_high, sunlight_low, sunlight_high, temperature_low, temperature_high, watering, plant_info, plant_web):
        self.id = id
        self.name = name
        self.plant_image = image
        self.plant_ph_high = plant_ph_high
        self.plant_ph_low = plant_ph_low
        self.sunlight_high = sunlight_high
        self.sunlight_low = sunlight_low
        self.temperature_high = temperature_high
        self.temperature_low = temperature_low
        self.watering = watering
        self.plant_info = plant_info
        self.plant_web = plant_web

        self.plant_tk = PlantTk()
