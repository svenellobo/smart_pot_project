

class ValuesDto:

    def __init__(self, id, ph, sun, temp, watering, plant_id, pot_id):
        self.id = id
        self.ph_value = ph
        self.sunlight_value = sun
        self.temperature_value = temp
        self.watering = watering
        self.plant_id = plant_id
        self.pot_id = pot_id



    def __repr__(self):
        return f"{self.ph_value}, {self.sunlight_value}, {self.temperature_value}, {self.watering}, {self.plant_id}, {self.pot_id}"