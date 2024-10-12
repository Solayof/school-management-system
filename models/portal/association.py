#!/usr/bin/python3

from sqlalchemy import Column, ForeignKey, String, Table
from models.base import Base


course_teacher_asso = Table("subjects_teachers",
    Base.metadata,
    Column("teacher_id", String(36), ForeignKey("teachers._id")),
    Column("course_id", String(36), ForeignKey("courses.id"))
)

exam_questions_asso = Table("examinations_questions",
    Base.metadata,
    Column("questions_id", String(36), ForeignKey("questions.id")),
    Column("examination_id", String(36), ForeignKey("examinations.id"))
)

student_courses_asso = Table("students_subjects",
    Base.metadata,
    Column("student_id", String(36), ForeignKey("students._id")),
    Column("course_id", String(36), ForeignKey("courses.id"))
)

course_class_asso = Table("classes_courses",
    Base.metadata,
    Column("class_id", String(36), ForeignKey("classes.id")),
    Column("course_id", String(36), ForeignKey("courses.id"))
)
