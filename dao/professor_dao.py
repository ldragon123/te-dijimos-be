from dao.database import Professor
from dao.database import DatabaseConnection
from dao.database_exception import Database_Exception
from sqlalchemy import func, desc, asc


class Professor_Dao:
    def get_professor_list(self):
        try:
            tmpSession = self.get_connection()
            professor_list = tmpSession.query(Professor)
            return professor_list

        except Exception as ex:
            raise Database_Exception(str(ex))

    # Ignores upper-lower case
    def get_professor(self, professor: Professor):
        try:
            tmpSession = self.get_connection()
            queriedProfessor = tmpSession.query(Professor).filter(func.lower(Professor.lastname) == func.lower(
                professor.lastname)).filter(func.lower(Professor.firstname) == func.lower(professor.firstname)).first()
            return queriedProfessor

        except Exception as ex:
            raise Database_Exception(str(ex))

    def search_professor(self, name):
        try:
            tmpSession = self.get_connection()
            search = "%{}%".format(name)
            results = tmpSession.query(Professor).filter(
                Professor.lastname.like(search)).all()
            return results
        except Exception as ex:
            raise Database_Exception(str(ex))

    def create_professor(self, professor: Professor):
        try:
            tmpSession = self.get_connection()
            tmpSession.add(professor)
            tmpSession.commit()
        except Exception as ex:
            raise Database_Exception(str(ex))

    def set_avg_score(self, professor_id, score):
        try:
            tmpSession = self.get_connection()
            professor = tmpSession.query(Professor).filter(
                Professor.id == professor_id).first()
            professor.score = score
            tmpSession.commit()
        except Exception as ex:
            raise Database_Exception(str(ex))

    def set_avg_difficulty(self, professor_id, difficulty):
        try:
            tmpSession = self.get_connection()
            professor = tmpSession.query(Professor).filter(
                Professor.id == professor_id).first()
            professor.difficulty = difficulty
            tmpSession.commit()
        except Exception as ex:
            raise Database_Exception(str(ex))

    def get_best_professors(self):
        try:
            tmpSession = self.get_connection()
            best_professors_list = tmpSession.query(
                Professor).order_by(desc(Professor.score)).limit(3)

        except Exception as ex:
            raise Database_Exception(str(ex))

        return best_professors_list

    def get_worst_professors(self):
        try:
            tmpSession = self.get_connection()
            best_professors_list = tmpSession.query(Professor).filter(
                Professor.score != None).order_by(asc(Professor.score)).limit(3)

        except Exception as ex:
            raise Database_Exception(str(ex))

        return best_professors_list

    def get_toughest_professors(self):
        try:
            tmpSession = self.get_connection()
            best_professors_list = tmpSession.query(
                Professor).order_by(desc(Professor.difficulty)).limit(3)

        except Exception as ex:
            raise Database_Exception(str(ex))

        return best_professors_list

    def get_easiest_professors(self):
        try:
            tmpSession = self.get_connection()
            best_professors_list = tmpSession.query(Professor).filter(
                Professor.difficulty != None).order_by(asc(Professor.difficulty)).limit(3)
        except Exception as ex:
            raise Database_Exception(str(ex))

        return best_professors_list

    def delete_professor(self, id):
        try:
            tmpSession = self.get_connection()
            tmpSession.query(Professor).filter(Professor.id == id).delete()
            tmpSession.commit()
        except Exception as ex:
            raise Database_Exception(str(ex))

    def get_connection(self):
        database = DatabaseConnection()
        tmpSession = database.get_session_for_database_created()

        return tmpSession
