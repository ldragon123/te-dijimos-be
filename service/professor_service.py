from dao.database import Professor
from dao.professor_dao import Professor_Dao
from dao.database_exception import Database_Exception
from service.service_exception import Service_Exception


class Professor_Service:
    def get_professor_list(self):
        try:
            professor_dao = Professor_Dao()
            return professor_dao.get_professor_list()
        except Database_Exception as ex:
            raise Service_Exception(str(ex))

    def get_professor(self, lastname, firstname):
        try:
            professor = Professor(firstname=firstname, lastname=lastname)
            professor_dao = Professor_Dao()
            return professor_dao.get_professor(professor)
        except Database_Exception as ex:
            raise Service_Exception(str(ex))

    def search_professor(self, name):
        try:
            professor_dao = Professor_Dao()
            return professor_dao.search_professor(name)
        except Database_Exception as ex:
            raise Service_Exception(str(ex))

    def create_professor(self, firstname, lastname, school):
        try:
            professor = Professor(firstname=firstname, lastname=lastname)
            professor_dao = Professor_Dao()

            # Checks if professor already exists
            databaseProfessor = professor_dao.get_professor(professor)

            if (databaseProfessor):
                return 'Professor Already Exists'
            else:
                professor_dao.create_professor(professor)
                return 'Professor Created'

        except Database_Exception as ex:
            raise Service_Exception(str(ex))

    def get_professor_from_name(self, professor):
        try:
            lastname = professor.split(', ')[0]
            firstname = professor.split(', ')[1]
            professor = Professor(firstname=firstname, lastname=lastname)
            professor_dao = Professor_Dao()
            return professor_dao.get_professor(professor)
        except Database_Exception as ex:
            raise Service_Exception(str(ex))

    def set_avg_score(self, professor_id, score):
        try:
            professor_dao = Professor_Dao()
            professor_dao.set_avg_score(professor_id, score)
        except Database_Exception as ex:
            raise Service_Exception(str(ex))

    def set_avg_difficulty(self, professor_id, difficulty):
        try:
            professor_dao = Professor_Dao()
            professor_dao.set_avg_difficulty(professor_id, difficulty)
        except Database_Exception as ex:
            raise Service_Exception(str(ex))

    def get_category(self, category):
        try:
            professor_dao = Professor_Dao()

            if(category == 'best_professors'):

                return professor_dao.get_best_professors()

            elif(category == 'worst_professors'):

                return professor_dao.get_worst_professors()

            elif(category == 'toughest_professors'):

                return professor_dao.get_toughest_professors()

            elif(category == 'easiest_professors'):

                return professor_dao.get_easiest_professors()

        except Database_Exception as ex:
            raise Service_Exception(str(ex))

    def delete_professor(self, id):
        try:
            professor_dao = Professor_Dao()
            professor_dao.delete_professor(id)

        except Database_Exception as ex:
            raise Service_Exception(str(ex))