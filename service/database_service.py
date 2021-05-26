from dao.database import DatabaseConnection


class Database_Service:
    def create_database(self):
        conection = DatabaseConnection()
        conection.create_database()
