from utils.DButil import DBUtil
from datetime import datetime as dt
from datasource.dto.ValuesDto import ValuesDto



class ValuesRepository:

    TABLE_NAME = "saved_values"

    def __init__(self, db):
        self.db = db
        self.create_table()

    def create_table(self):
        query = f"""
            CREATE TABLE IF NOT EXISTS
            {self.TABLE_NAME} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,                        
                ph_value FLOAT NOT NULL,                                 
                sunlight_value INTEGER NOT NULL,                
                temperature_value INTEGER NOT NULL,                               
                watering DATETIME,                
                plant_id INTEGER NOT NULL,
                pot_id INTEGER NOT NULL,
                created DATETIME NOT NULL,
                FOREIGN KEY (pot_id) REFERENCES pot(id)
            );
        """
        DBUtil.execute_and_write(self.db, query)


    def add_values(self, ph_value, sunlight_value, temperature_value, watering, plant_id, pot_id):
        query = f"""
            INSERT INTO {self.TABLE_NAME} (ph_value, sunlight_value, temperature_value, watering, plant_id,
                                           pot_id, created)
            VALUES ({ph_value}, {sunlight_value}, {temperature_value}, '{watering}', {plant_id},
                    {pot_id}, '{dt.now()}');
        """
        DBUtil.execute_and_write(self.db, query)



    def get_old_watering_date(self, pot_id, plant_id):
        try:
            query = f"""SELECT watering FROM {self.TABLE_NAME} WHERE (pot_id = {pot_id} AND plant_id = {plant_id}) 
            ORDER BY id DESC LIMIT 1;
                """
            water_date = DBUtil.grab_data(self.db, query)
            if water_date is not None:
                return water_date[0]
        except:
            return None

    def fetch_all_values(self, pot_id, plant_id, single=True):
        if single == True:
            try:
                query = f"""SELECT * FROM {self.TABLE_NAME} WHERE (pot_id = {pot_id} AND plant_id = {plant_id}) 
                ORDER BY id DESC LIMIT 1;
                    """
                result = DBUtil.grab_data(self.db, query)
                if result is not None:
                    values = ValuesDto(result[0], result[1], result[2], result[3], result[4], result[5], result[6])
                    return values
            except:
                pass
        else:
            values_list = []
            try:
                query = f"""SELECT * FROM {self.TABLE_NAME} WHERE (pot_id = {pot_id} AND plant_id = {plant_id});                 
                    """
                result = DBUtil.fetch_data_list(self.db, query)
                #if result is not None:
                for value in result:
                    values: ValuesDto = ValuesDto(value[0], value[1], value[2], value[3], value[4], value[5], value[6])
                    values_list.append(values)
                return values_list
            except:
                pass
