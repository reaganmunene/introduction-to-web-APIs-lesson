from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Course(db.Model, SerializerMixin):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    duration = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    lecturer_id = db.Column(db.Integer, db.ForeignKey('lecturers.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))

    def __repr__(self):
        return f'<Course {self.title}>'

class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer)
    comment = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))

    def __repr__(self):
        return f'<Review ({self.id}) of {self.course}: {self.score}/10>'

class Lecturer(db.Model, SerializerMixin):
    __tablename__ = 'lecturers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    courses = db.relationship('Course', backref='lecturer')

    def __repr__(self):
        return f'<Lecturer {self.name}>'

class Student(db.Model, SerializerMixin):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    reviews = db.relationship('Review', backref='student')
    courses = db.relationship('Course', backref='student')

    def __repr__(self):
        return f'<Student {self.name}>'
