from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class Course(db.Model, SerializerMixin):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    reviews = db.relationship('Review', backref='course')
    lecturers = db.relationship('Lecturer', secondary='course_lecturer', back_populates='courses')

    def to_dict(self):
        # Avoid serialization of the entire related models to prevent recursion
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description
        }

class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer)
    comment = db.Column(db.String)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))

    def to_dict(self):
        # Avoid serialization of the entire related models to prevent recursion
        return {
            'id': self.id,
            'score': self.score,
            'comment': self.comment,
            'course_id': self.course_id,
            'student_id': self.student_id
        }

class Lecturer(db.Model, SerializerMixin):
    __tablename__ = 'lecturers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    courses = db.relationship('Course', secondary='course_lecturer', back_populates='lecturers')

    def to_dict(self):
        # Avoid serialization of the entire related models to prevent recursion
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }

class Student(db.Model, SerializerMixin):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    reviews = db.relationship('Review', backref='student')

    def to_dict(self):
        # Avoid serialization of the entire related models to prevent recursion
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }

course_lecturer = db.Table('course_lecturer',
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id')),
    db.Column('lecturer_id', db.Integer, db.ForeignKey('lecturers.id'))
)

