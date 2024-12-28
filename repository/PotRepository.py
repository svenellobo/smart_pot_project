from utils.DButil import DBUtil
from datasource.dto.PotDto import PotDto




class PotRepository:
    
    TABLE_NAME = "pots"

    
    def __init__(self, db):
        self.db = db
        self.create_table()


    def create_table(self):
        query = f"""
        CREATE TABLE IF NOT EXISTS
        {self.TABLE_NAME} (
            id  INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(30) NOT NULL,
            image VARCHAR(30) NOT NULL,                        
            plant_id INTEGER NULL,
            FOREIGN KEY (plant_id) REFERENCES plants(id)
        );
        """
        DBUtil.execute_and_write(self.db, query)

    def add_pot(self, name, img):
        query = f"""
            INSERT INTO {self.TABLE_NAME} (name, image)
            VALUES ('{name}', '{img}');

        """
        DBUtil.execute_and_write(self.db, query)


    def fetch_pot_by_id(self, id):
        query = f"SELECT * FROM {self.TABLE_NAME} WHERE id = {id};"
        selected_pot = DBUtil.grab_data(self.db, query)

        if selected_pot is not None:
            pot: PotDto = PotDto(selected_pot[0], selected_pot[1], selected_pot[2], selected_pot[3])
            return pot
        else:
            return None


    def update_pot(self, pot: PotDto, full_update=False):
        if pot is not None:
            if full_update == False:
                query = f"""
                        UPDATE {self.TABLE_NAME} SET name='{pot.name}',
                                                     image='{pot.pot_img}'                                                                                                     
                        WHERE id={pot.id};        
                        """
                DBUtil.execute_and_write(self.db, query)
            else:
                query = f"""
                        UPDATE {self.TABLE_NAME} SET name='{pot.name}',
                                                     image='{pot.pot_img}',
                                                     plant_id={pot.plant_id}                                                 
                        WHERE id={pot.id};        
                        """
                DBUtil.execute_and_write(self.db, query)

    def find_all_pots(self):
        all_pots = []
        query = f"""
                    SELECT * from {self.TABLE_NAME}; 
                """

        pots = DBUtil.fetch_data_list(self.db, query)
        for attribute in pots:
            pot: PotDto = PotDto(attribute[0], attribute[1], attribute[2], attribute[3])
            all_pots.append(pot)
        return all_pots

    def delete_pot(self, pot: PotDto):
        if pot is not None:
            query = f"""DELETE FROM {self.TABLE_NAME} WHERE id={pot.id};"""
            DBUtil.execute_and_write(self.db, query)



    def empty_pot(self, pot:PotDto):
        if pot is not None:
            query = f"""
                        UPDATE {self.TABLE_NAME} SET name='{pot.name}',
                                                     image='{pot.pot_img}',                                                     
                                                     plant_id=NULL
                                                                                                     
                        WHERE id={pot.id};        
                        """
            DBUtil.execute_and_write(self.db, query)



