from sqlalchemy import Boolean, Column, ForeignKey, Integer, String , DateTime
from sqlalchemy.orm import relationship

from .database import Base

class Mentor(Base):
    __tablename__ = "mentors"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    password = Column(String)
    registered_at = Column(DateTime)
    role = Column(String)
    is_active = Column(Boolean, default=True)

    students = relationship("Student", back_populates="mentor")
    payments = relationship("Payment", back_populates="mentor")

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    birth_date = Column(DateTime)
    degree_id = Column(Integer, ForeignKey("degrees.id"))
    classroom_id = Column(Integer, ForeignKey("classrooms.id"))
    mentor_id = Column(Integer, ForeignKey("mentors.id"))
    state = Column(String)

    degree = relationship("Degree", back_populates="students")
    classroom = relationship("Classroom", back_populates="students")
    mentor = relationship("Mentor", back_populates="students")
    attendances = relationship("Attendance", back_populates="student")


class Degree(Base):
    __tablename__ = "degrees"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    level = Column(String)

    students = relationship("Student", back_populates="degree")
    classroom = relationship("Classroom", back_populates="degree")
    courses = relationship("Course", back_populates="degree")


class Classroom(Base):
    __tablename__ = "classrooms"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    degree_id = Column(Integer, ForeignKey("degrees.id"))
    capacity = Column(Integer)
    day = Column(String)
    time_slot = Column(String)

    students = relationship("Student", back_populates="classroom")
    degree = relationship("Degree", back_populates="classroom")

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    duration = Column(Integer)
    degree_id = Column(Integer, ForeignKey("degrees.id"))

    degree = relationship("Degree", back_populates="courses")
    attendances = relationship("Attendance", back_populates="course")

class Attendance(Base):
    __tablename__ = "attendances"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date = Column(DateTime)
    student_id = Column(Integer, ForeignKey("students.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))

    student = relationship("Student", back_populates="attendances")
    course = relationship("Course", back_populates="attendances")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)


    def __repr__(self):
        return f"<User {self.username}>"
    
    def __str__(self):
        return f"{self.username}"
    
class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    amount = Column(Integer)
    date = Column(DateTime)
    method = Column(String)
    state = Column(String)
    quarter = Column(String)
    mentor_id = Column(Integer, ForeignKey("mentors.id"))
    student_id = Column(Integer, ForeignKey("students.id"))

    mentor = relationship("Mentor", back_populates="payments")


