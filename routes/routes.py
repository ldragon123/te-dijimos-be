from flask import Flask, request, jsonify, Response, json
from service.review_service import Review_Service
from service.professor_service import Professor_Service
from service.database_service import Database_Service
from flask_cors import CORS, cross_origin

from service.service_exception import Service_Exception

app = Flask(__name__)
CORS(app)

# we create the db from this endpoint only for educational purposes
# @app.route('/create_database', methods=['GET'])
# def create_database():
#     database_service = Database_Service()
#     database_service.create_database()
#     success = True

#     return jsonify(result=success)


@app.route('/create_professor', methods=['POST'])
def create_professor():
    data = request.form
    first_name = data['first_name']
    last_name = data['last_name']
    school = data['school']
    professor_service = Professor_Service()

    first_name = first_name.strip()
    last_name = last_name.strip()

    validator = True

    if(len(first_name) < 4 or len(first_name) > 20):
        validator = False
    if(len(last_name) < 4 or len(last_name) > 20):
        validator = False
    if(len(school) < 4 or len(school) > 40):
        validator = False

    if (validator == True):
        try:
            response = professor_service.create_professor(
                first_name, last_name, school)
        except Service_Exception as ex:
            return Response(str(ex), status=500)

        return Response(response, status=201)
    else:
        return Response('Professor not created', status=201)


@app.route('/create_review', methods=['POST'])
def create_review():
    data = request.form

    title = data['title']
    description = data['description']
    professor_name = data['professor']
    score = data['score']
    difficulty = data['difficulty']
    course = data['class']

    score = int(score)
    difficulty = int(difficulty)

    validator = True

    if (len(title) < 4 or len(title) > 35):
        validator = False
    elif (len(description) < 4 or len(description) > 700):
        validator = False
    elif (score < 1 or score > 10 or (isinstance(score, int) != True)):
        validator = False
    elif (difficulty < 1 or difficulty > 10 or (isinstance(difficulty, int) != True)):
        validator = False
    elif (len(course) < 4 or len(course) > 30):
        validator = False
    if (validator == True):

        review_service = Review_Service()

        try:
            review_service.create_review(
                title, description, professor_name, course, score, difficulty)

        except Service_Exception as ex:
            return Response(str(ex), status=500)

        return Response('Review Created', status=201, mimetype='application/json')

    else:

        return Response('Review not Created', status=500)


@app.route('/get_review/<int:id>', methods=['GET'])
def get_review(id):
    review_service = Review_Service()

    try:
        response = review_service.get_review(id)

    except Service_Exception as ex:
        return Response(str(ex), status=500)

    return Response(json.dumps(response.to_dict()), status=200, mimetype='application/json')


@app.route('/get_reviews_from_professor/<string:professor>', methods=['GET'])
def get_reviews_from_professor(professor):
    review_service = Review_Service()

    try:
        response = review_service.get_reviews_from_professor(professor)

    except Service_Exception as ex:
        return Response(str(ex), status=500)

    return Response(json.dumps([review.to_dict() for review in response]), status=200, mimetype='application/json')


@app.route('/review_list', methods=['GET'])
def review_list():
    review_service = Review_Service()

    try:
        response = review_service.get_review_list()

    except Service_Exception as ex:
        return Response(str(ex), status=500)

    return Response(json.dumps([review.to_dict() for review in response]), status=200, mimetype='application/json')


@app.route('/delete_review/<int:id>', methods=['DELETE'])
def delete_review(id):
    review_service = Review_Service()

    try:
        review_service.delete_review(id)

    except Service_Exception as ex:
        return Response(str(ex), status=500)

    return Response('review successfully deleted', status=204)


@app.route('/delete_professor/<int:id>', methods=['DELETE'])
def delete_professor(id):
    professor_service = Professor_Service()

    try:
        professor_service.delete_professor(id)

    except Service_Exception as ex:
        return Response(str(ex), status=500)

    return Response('professor successfully deleted', status=204)


@app.route('/professor_list', methods=['GET'])
def professor_list():
    professor_service = Professor_Service()

    try:
        response = professor_service.get_professor_list()

    except Service_Exception as ex:
        return Response(str(ex), status=500)

    return Response(json.dumps([professor.to_dict() for professor in response]), status=200, mimetype='application/json')


@app.route('/search_professor/<string:name>', methods=['GET'])
def search_professor(name):
    professor_service = Professor_Service()

    try:
        response = professor_service.search_professor(name)

    except Service_Exception as ex:
        return Response(str(ex), status=500)

    return Response(json.dumps([professor.to_dict() for professor in response]), status=200, mimetype='application/json')


@app.route('/get_professor_from_name/<string:professor>', methods=['GET'])
def get_professor_from_name(professor):
    professor_service = Professor_Service()

    try:
        response = professor_service.get_professor_from_name(professor)

    except Service_Exception as ex:
        return Response(str(ex), status=500)

    return Response(json.dumps(response.to_dict()), status=200, mimetype='application/json')


@app.route('/get_professor_from_category/<string:category>', methods=['GET'])
def get_professor_from_category(category):
    professor_service = Professor_Service()

    try:
        response = professor_service.get_category(category)
    except Service_Exception as ex:
        return Response(str(ex), status=500)

    return Response(json.dumps([professor.to_dict() for professor in response]), status=200, mimetype='application/json')
