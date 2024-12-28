from sqlite3 import Connection, Cursor

class DBUtil:

    @staticmethod
    def execute_and_write(db: Connection, query):
        try:
            cursor: Cursor = db.cursor()
            cursor.execute(query)
            db.commit()
            cursor.close()
            return True
        except Exception as e:
            print(e)
        return False


    @staticmethod
    def grab_data(db: Connection, query):
        try:
            cursor: Cursor = db.cursor()
            cursor.execute(query)
            rezultat = cursor.fetchone()
            cursor.close()
            return rezultat
        except Exception as e:
            print(e)
            return None



    @staticmethod
    def fetch_data_list(db: Connection, query):
        try:
            cursor: Cursor = db.cursor()
            cursor.execute(query)
            rezultat = cursor.fetchall()
            cursor.close()
            return rezultat
        except Exception as e:
            print(e)
