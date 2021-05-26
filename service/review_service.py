from dao.database import Review
from dao.review_dao import Review_Dao
from service.professor_service import Professor_Service
from dao.database_exception import Database_Exception
from service.service_exception import Service_Exception
from dao.professor_dao import Professor_Dao
from dao.database import Professor


class Review_Service:
    def create_review(self, title, description, professor_name, course, score, difficulty):
        try:
            professor_last_name = professor_name.split(', ')[0]
            professor_first_name = professor_name.split(', ')[1]

            professor_service = Professor_Service()
            professor_object = professor_service.get_professor(
                professor_last_name, professor_first_name)

            review = Review(title=title, description=description, professor_id=professor_object.id,
                            course=course, score=score, difficulty=difficulty)
            review_dao = Review_Dao()
            review_dao.create_review(review)

            avg_score = review_dao.get_avg_review_score(professor_object.id)
            avg_difficulty = review_dao.get_avg_review_difficulty(
                professor_object.id)

            professor_service.set_avg_score(professor_object.id, avg_score)
            professor_service.set_avg_difficulty(
                professor_object.id, avg_difficulty)

        except Database_Exception as ex:
            raise Service_Exception(str(ex))

    def get_review(self, id):
        try:
            review_dao = Review_Dao()
            return review_dao.get_review(id)
        except Database_Exception as ex:
            raise Service_Exception(str(ex))

    def get_reviews_from_professor(self, professor_name):

        professor_last_name = professor_name.split(', ')[0]
        professor_first_name = professor_name.split(', ')[1]

        try:
            professor_service = Professor_Service()
            professor_object = professor_service.get_professor(
                professor_last_name, professor_first_name)

            review_dao = Review_Dao()
            return review_dao.get_reviews_from_professor(professor_object.id)

        except Database_Exception as ex:
            raise Service_Exception(str(ex))

    def get_review_list(self):
        try:
            review_dao = Review_Dao()
            return review_dao.get_review_list()

        except Database_Exception as ex:
            raise Service_Exception(str(ex))

    def delete_review(self, id):
        try:
            review_dao = Review_Dao()
            review_dao.delete_review(id)

        except Database_Exception as ex:
            raise Service_Exception(str(ex))

    def modify_review_description(self, id, description):
        try:
            review_dao = Review_Dao()
            review_dao.modify_review_description(id, description)

        except Database_Exception as ex:
            raise Service_Exception(str(ex))
