#!/usr/bin/env python3

from random import randint, choice as rc
from faker import Faker
from app import app
from models import db, Course, Review, Lecturer, Student

lecturers = [
    "Dr. Smith",
    "Prof. Johnson",
    "Dr. Williams",
    "Prof. Brown",
    "Dr. Jones",
    "Prof. Miller",
    "Dr. Davis",
    "Prof. Garcia",
    "Dr. Rodriguez",
    "Prof. Martinez",
    "Dr. Hernandez",
    "Prof. Lopez",
    "Dr. Gonzalez",
    "Prof. Wilson",
    "Dr. Anderson",
    "Prof. Thomas",
    "Dr. Taylor",
    "Prof. Moore",
    "Dr. Jackson",
    "Prof. Martin",
    "Dr. Lee",
    "Prof. Perez",
    "Dr. Thompson",
    "Prof. White",
    "Dr. Harris"
]

students = [
    "Alice",
    "Bob",
    "Charlie",
    "David",
    "Eve",
    "Frank",
    "Grace",
    "Heidi",
    "Ivan",
    "Judy",
    "Mallory",
    "Niaj",
    "Olivia",
    "Peggy",
    "Sybil",
    "Trent",
    "Victor",
    "Walter",
    "Xander",
    "Yvonne",
    "Zara",
    "Liam",
    "Noah",
    "Emma",
    "Olivia"
]

fake = Faker()

with app.app_context():

    Review.query.delete()
    Student.query.delete()
    Lecturer.query.delete()
    Course.query.delete()

    students_list = []
    for name in students:
        s = Student(name=name)
        students_list.append(s)

    db.session.add_all(students_list)

    lecturers_list = []
    for name in lecturers:
        l = Lecturer(name=name)
        lecturers_list.append(l)

    db.session.add_all(lecturers_list)

    courses = []
    for i in range(100):
        c = Course(
            title=fake.sentence(),
            lecturer=rc(lecturers_list),
            student=rc(students_list),
            duration=randint(1, 4),
        )
        courses.append(c)

    db.session.add_all(courses)

    reviews = []
    for s in students_list:
        for i in range(randint(1, 10)):
            r = Review(
                score=randint(0, 10),
                comment=fake.sentence(),
                student=s,
                course=rc(courses))
            reviews.append(r)

    db.session.add_all(reviews)

    db.session.commit()
