from dao.database import Review, Professor
from dao.database import DatabaseConnection
from dao.database_exception import Database_Exception
from sqlalchemy import func, desc, distinct


class Review_Dao:

    def create_review(self, review: Review):
        try:
            tmpSession = self.get_connection()
            tmpSession.add(review)
            tmpSession.commit()
        except Exception as ex:
            raise Database_Exception(str(ex))

    def get_review(self, id):
        try:
            tmpSession = self.get_connection()
            queriedReview = tmpSession.query(
                Review).filter(Review.id == id).first()
            return queriedReview
        except Exception as ex:
            raise Database_Exception(str(ex))

    def get_reviews_from_professor(self, professor_id):
        try:
            tmpSession = self.get_connection()
            queriedReview = tmpSession.query(Review).filter(
                Review.professor_id == professor_id)
            return queriedReview
        except Exception as ex:
            raise Database_Exception(str(ex))

    def get_review_list(self):
        try:
            tmpSession = self.get_connection()
            review_list = tmpSession.query(Review)
            return review_list
        except Exception as ex:
            raise Database_Exception(str(ex))

    def delete_review(self, id):
        try:
            tmpSession = self.get_connection()
            tmpSession.query(Review).filter(Review.id == id).delete()
            tmpSession.commit()
        except Exception as ex:
            raise Database_Exception(str(ex))

    def delete_from_professor(self, professor_id):
        try:
            tmpSession = self.get_connection()
            tmpSession.query(Review).filter(Review.professor_id == professor_id).delete()
            tmpSession.commit()

        except Exception as ex:
            raise Database_Exception(str(ex))

    def modify_review_description(self, id, description):
        try:
            tmpSession = self.get_connection()
            review = tmpSession.query(Review).filter(Review.id == id).first()
            review.description = description
            tmpSession.commit()
        except Exception as ex:
            raise Database_Exception(str(ex))

    def get_avg_review_score(self, prof_id):
        try:
            tmpSession = self.get_connection()
            avg_score = tmpSession.query(func.avg(Review.score)).filter(
                Review.professor_id == prof_id).scalar()
            return avg_score
        except Exception as ex:
            raise Database_Exception(str(ex))

    def get_avg_review_difficulty(self, prof_id):
        try:
            tmpSession = self.get_connection()
            avg_difficulty = tmpSession.query(func.avg(Review.difficulty)).filter(
                Review.professor_id == prof_id).scalar()
            return avg_difficulty
        except Exception as ex:
            raise Database_Exception(str(ex))

    def get_last_reviews(self):
        try:
            tmpSession = self.get_connection()
            review_list = tmpSession.query(Review.description, Professor.lastname, Professor.firstname).join(Professor).filter(Professor.firstname != "Universidad").order_by(desc(Review.id)).limit(3)
            return review_list
        except Exception as ex:
            raise Database_Exception(str(ex))

    def get_review_stats(self):
        try:
            tmpSession = self.get_connection()
            review_stats = tmpSession.query(func.count(Review.id)).first()
            return review_stats

        except Exception as ex:
            raise Database_Exception(str(ex))
        
    def get_full_review_from_id(self, id):
        try:
            tmpSession = self.get_connection()
            queriedReview = tmpSession.query(Review).filter(
                Review.id == id)

            return queriedReview

        except Exception as ex:
            raise Database_Exception(str(ex))

    
    def get_connection(self):
        database = DatabaseConnection()
        tmpSession = database.get_session_for_database_created()

        return tmpSession

