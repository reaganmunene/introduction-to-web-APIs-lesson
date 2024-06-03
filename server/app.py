#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

from models import db, Course, Review, Lecturer, Student

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return "Index for Course/Review/Lecturer/Student API"

@app.route('/courses')
def courses():

    courses = []
    for course in Course.query.all():
        course_dict = course.to_dict()
        courses.append(course_dict)

    response = make_response(
        courses,
        200
    )

    return response

@app.route('/courses/<int:id>')
def course_by_id(id):
    course = Course.query.filter(Course.id == id).first()

    course_dict = course.to_dict()

    response = make_response(
        course_dict,
        200
    )

    return response

@app.route('/reviews', methods=['GET', 'POST'])
def reviews():

    if request.method == 'GET':
        reviews = []
        for review in Review.query.all():
            review_dict = review.to_dict()
            reviews.append(review_dict)

        response = make_response(
            reviews,
            200
        )

        return response

    elif request.method == 'POST':
        new_review = Review(
            score=request.form.get("score"),
            comment=request.form.get("comment"),
            course_id=request.form.get("course_id"),
            student_id=request.form.get("student_id"),
        )

        db.session.add(new_review)
        db.session.commit()

        review_dict = new_review.to_dict()

        response = make_response(
            review_dict,
            201
        )

        return response

@app.route('/reviews/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def review_by_id(id):
    review = Review.query.filter(Review.id == id).first()

    if review == None:
        response_body = {
            "message": "This record does not exist in our database. Please try again."
        }
        response = make_response(response_body, 404)

        return response

    else:
        if request.method == 'GET':
            review_dict = review.to_dict()

            response = make_response(
                review_dict,
                200
            )

            return response

        elif request.method == 'PATCH':
            for attr in request.form:
                setattr(review, attr, request.form.get(attr))

            db.session.add(review)
            db.session.commit()

            review_dict = review.to_dict()

            response = make_response(
                review_dict,
                200
            )

            return response

        elif request.method == 'DELETE':
            db.session.delete(review)
            db.session.commit()

            response_body = {
                "delete_successful": True,
                "message": "Review deleted."
            }

            response = make_response(
                response_body,
                200
            )

            return response

@app.route('/students')
def students():

    students = []
    for student in Student.query.all():
        student_dict = student.to_dict()
        students.append(student_dict)

    response = make_response(
        students,
        200
    )

    return response

@app.route('/lecturers')
def lecturers():

    lecturers = []
    for lecturer in Lecturer.query.all():
        lecturer_dict = lecturer.to_dict()
        lecturers.append(lecturer_dict)

    response = make_response(
        lecturers,
        200
    )

    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
