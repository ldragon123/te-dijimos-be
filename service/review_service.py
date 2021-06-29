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

            # Gets the averages from db
            avg_score = review_dao.get_avg_review_score(professor_object.id)
            avg_difficulty = review_dao.get_avg_review_difficulty(
                professor_object.id)

            # Sets the averages to Professor
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

            review_object = review_dao.get_full_review_from_id(id)
            review = review_object[0].to_dict()
            professor_id = review["professor_id"]

            review_dao.delete_review(id)

            # After deleting the review, it sets the new average for professor table
            avg_score = review_dao.get_avg_review_score(professor_id)
            avg_difficulty = review_dao.get_avg_review_difficulty(professor_id)

            professor_service = Professor_Service()

            professor_service.set_avg_score(professor_id, avg_score)
            professor_service.set_avg_difficulty(professor_id, avg_difficulty)

        except Database_Exception as ex:
            raise Service_Exception(str(ex))

    def modify_review_description(self, id, description):
        try:
            review_dao = Review_Dao()
            review_dao.modify_review_description(id, description)

        except Database_Exception as ex:
            raise Service_Exception(str(ex))

    def get_last_reviews(self):
        try:
            review_dao = Review_Dao()
            reviews = review_dao.get_last_reviews()

            # It creates an empty dictionary
            aux_reviews = [{"description": "", "lastname": "", "firstname": "" }, 
            {"description": "", "lastname": "", "firstname": "" }, 
            {"description": "", "lastname": "", "firstname": "" }]

            # It fills the dictionary with the review information
            index = 0
            while(index < 3):
                aux_reviews[index]["description"] = reviews[index][0]
                aux_reviews[index]["lastname"] = reviews[index][1]
                aux_reviews[index]["firstname"] = reviews[index][2]
                index = index + 1

            return aux_reviews

        except Database_Exception as ex:
            raise Service_Exception(str(ex))

    def get_review_stats(self):
        try:
            review_dao = Review_Dao()
            stats = review_dao.get_review_stats()
            return stats[0]

        except Database_Exception as ex:
            raise Service_Exception(str(ex))


    def delete_from_professor(self, professor_id):
        try:
            review_dao = Review_Dao()
            review_dao.delete_from_professor(professor_id)

        except Database_Exception as ex:
            raise Service_Exception(str(ex))