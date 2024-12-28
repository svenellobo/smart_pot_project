from datasource.dto.PlantDto import PlantDto
from datasource.tk.PotTk import PotTk



class PotDto():

    def __init__(self, id, name, pot_img, plant_id):
        self.id = id
        self.name = name
        self.pot_img = pot_img
        self.plant_id = plant_id
        self.pot_tk = PotTk()
        self.plant: PlantDto = None

