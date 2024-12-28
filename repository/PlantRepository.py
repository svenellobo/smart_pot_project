import os.path

from utils.DButil import DBUtil
from datasource.dto.PlantDto import PlantDto

class PlantRepository:

    TABLE_NAME = "plants"

    def __init__(self, db):
        self.db = db
        self.create_table()
        self._add_plants()



    def create_table(self):
        query = f"""
            CREATE TABLE IF NOT EXISTS
            {self.TABLE_NAME} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(30) NOT NULL,
                plant_image VARCHAR(50) NULL,                
                plant_ph_low FLOAT NOT NULL,
                plant_ph_high FLOAT NOT NULL,                 
                sunlight_low INTEGER NOT NULL,
                sunlight_high INTEGER NOT NULL,
                temperature_low INTEGER NOT NULL,
                temperature_high INTEGER NOT NULL,                
                watering INTEGER NOT NULL,
                plant_info INTEGER NULL,
                plant_web VARCHAR(50) NULL
            );
        """
        DBUtil.execute_and_write(self.db, query)


    def add_plant(self, name, plant_image, plant_ph_low, plant_ph_high, sunlight_low, sunlight_high, temperature_low, temperature_high, watering, plant_info, plant_web):
        query = f"""
            INSERT INTO {self.TABLE_NAME} (name, plant_image, plant_ph_low, plant_ph_high, sunlight_low, sunlight_high,
                                           temperature_low, temperature_high, watering, plant_info, plant_web)
            VALUES ('{name}', '{plant_image}', {plant_ph_low}, {plant_ph_high}, {sunlight_low}, {sunlight_high},
                    {temperature_low}, {temperature_high}, {watering}, '{plant_info}', '{plant_web}');
        """
        DBUtil.execute_and_write(self.db, query)


    def find_all_plants(self):
        all_plants = []
        query = f"""
            SELECT * from {self.TABLE_NAME}; 
        """
        plants = DBUtil.fetch_data_list(self.db, query)
        for attribute in plants:
            plant: PlantDto = PlantDto(attribute[0], attribute[1], attribute[2], attribute[3],
                                       attribute[4], attribute[5], attribute[6],
                                       attribute[7], attribute[8], attribute[9], attribute[10], attribute[11])
            all_plants.append(plant)
        return all_plants


    def update_plant(self, plant: PlantDto):
        if plant is not None:
            query = f"""
            UPDATE {self.TABLE_NAME} SET name='{plant.name}',
                                         plant_image='{plant.plant_image}',
                                         plant_ph_low={plant.plant_ph_low},
                                         plant_ph_high={plant.plant_ph_high},
                                         sunlight_low={plant.sunlight_low},
                                         sunlight_high={plant.sunlight_high},
                                         temperature_low={plant.temperature_low},
                                         temperature_high={plant.temperature_high},                                         
                                         watering={plant.watering},                                         
                                         plant_info='{plant.plant_info}'
                                         
            WHERE id={plant.id};
        """
            DBUtil.execute_and_write(self.db, query)


    def delete_plant(self, plant: PlantDto):
        if plant is not None:
            query = f"""DELETE FROM {self.TABLE_NAME} WHERE id={plant.id};"""
            DBUtil.execute_and_write(self.db, query)


    def fetch_plant_by_id(self, id):
        query = f"""SELECT * FROM {self.TABLE_NAME} WHERE id = {id};"""

        entity = DBUtil.grab_data(self.db, query)
        if entity is not None:
            plant: PlantDto = PlantDto(entity[0], entity[1], entity[2], entity[3],
                                   entity[4], entity[5], entity[6],
                                   entity[7], entity[8], entity[9], entity[10], entity[11])
            return plant
        else:
            return None

    def _add_plants(self, db_path="Pyflora.db"):
        self.add_plant("Spatifilum", "./images/spatifilum.png", 5.8, 6.5, 3, 5, 20, 25, 3, "./images/plant_info/spatifilum.txt", "https://www.vrtlarica.hr/spatifilum-sadnja-uzgoj/")
        self.add_plant("Basil", "./images/basil.jpg", 4.3, 8.2, 6, 10, 15, 25, 7, "./images/plant_info/basil.txt", "https://www.vrtlarica.hr/bosiljak-sadnja-uzgoj/")
        self.add_plant("Oregano", "./images/oregano.jpg", 5.6, 7, 8, 12, 16, 26, 7, "./images/plant_info/oregano.txt", "https://www.vrtlarica.hr/sadnja-uzgoj-origana/")
        self.add_plant("Houseleek", "./images/houseleek.jpg", 6.0, 8.0, 6, 10, 5, 25, 30, "./images/plant_info/houseleek.txt", "https://www.vrtlarica.hr/cuvarkuca-sadnja-uzgoj/")
        self.add_plant("African violets", "./images/african_violets.jpg", 4.5, 5.5, 8, 10, 18, 24, 7, "./images/plant_info/african_violets.txt", "https://www.vrtlarica.hr/sadnja-uzgoj-africke-ljubicice/")
        self.add_plant("Kalanchoe", "./images/kalanchoe.jpg", 5, 6.5, 4, 6, 7, 21, 14, "./images/plant_info/kalanchoe.txt", "https://www.vrtlarica.hr/kalanhoa-sadnja-uzgoj/")
        self.add_plant("Hosta", "./images/hosta.jpg", 6.5, 7.5, 5, 6, -4, 30, 7, "./images/plant_info/hosta.txt", "https://www.vrtlarica.hr/hosta-sadnja-uzgoj/")
        self.add_plant("Mint", "./images/mint.jpg", 6.0, 7.0, 2, 5, 13, 21, 3, "./images/plant_info/mint.txt", "https://www.vrtlarica.hr/metvica-menta-sadnja-uzgoj/")
        self.add_plant("Rosemary", "./images/rosemary.jpg", 6.5, 7.0, 6, 8, 12, 26, 14, "./images/plant_info/rosemary.txt", "https://www.vrtlarica.hr/ruzmarin-sadnja-uzgoj/")
        self.add_plant("Sage", "./images/sage.jpg", 6.0, 7.0, 6, 8, 15, 21, 5, "./images/plant_info/sage.txt", "https://www.vrtlarica.hr/kadulja-zalfija-sadnja-uzgoj/" )