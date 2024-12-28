from sqlite3 import Connection, Cursor

class DBUtil:

    @staticmethod
    def execute_and_write(db: Connection, upit):
        try:
            cursor: Cursor = db.cursor()
            cursor.execute(upit)
            db.commit()
            cursor.close()
            return True
        except Exception as e:
            print(e)
        return False


    @staticmethod
    def grab_data(db: Connection, upit):
        try:
            cursor: Cursor = db.cursor()
            cursor.execute(upit)
            rezultat = cursor.fetchone()
            cursor.close()
            return rezultat
        except Exception as e:
            print(e)
            return None



    @staticmethod
    def fetch_data_list(db: Connection, upit):
        try:
            cursor: Cursor = db.cursor()
            cursor.execute(upit)
            rezultat = cursor.fetchall()
            cursor.close()
            return rezultat
        except Exception as e:
            print(e)
