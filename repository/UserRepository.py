from utils.DButil import DBUtil
from datasource.dto.UserDto import UserDto


class UserRepository:

    TABLE_NAME = "users"

    def __init__(self, db):
        self.db = db
        self.create_table()
        #self._create_user()



    def create_table(self):
        query = f"""
            CREATE TABLE IF NOT EXISTS
            {self.TABLE_NAME} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(30) NOT NULL,
                surname VARCHAR(30) NOT NULL,
                username VARCHAR(30) NOT NULL UNIQUE,
                password VARCHAR(30) NOT NULL
            );
        """
        DBUtil.execute_and_write(self.db, query, )

    def add_user(self, name, surname, username, password):
        query = f"""
            INSERT INTO {self.TABLE_NAME} (name, surname, username, password)
            VALUES ('{name}', '{surname}', '{username}', '{password}');
        """
        DBUtil.execute_and_write(self.db, query)

    def update_user(self, user: UserDto):
        if user is not None:
            query = f"""
            UPDATE {self.TABLE_NAME} SET name='{user.name}', surname='{user.surname}', username='{user.username}', password='{user.password}'
            WHERE id={user.id}
        """
            DBUtil.execute_and_write(self.db, query)


    def fetch_user(self, username, password):
        query = f"SELECT * FROM {self.TABLE_NAME} WHERE username = '{username}' and password = '{password}';"
        result = DBUtil.grab_data(self.db, query)
        if result is not None:
            user: UserDto = UserDto(result[0], result[1], result[2], result[3], result[4])
            return user
        else:
            return None


    def _create_user(self):
        self.add_user("John", "Smith", "user", "123")

    



