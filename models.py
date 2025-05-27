from datetime import datetime

from sqlalchemy import Integer, String, ForeignKey, func
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Student(Base):
    __tablename__ = 'students'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    group_id: Mapped[int] = mapped_column(
        ForeignKey('groups.id', ondelete='CASCADE'), nullable=False)
    group: Mapped['Group'] = relationship(
        'Group',
        back_populates='students'
    )
    grades: Mapped[list['Grade']] = relationship(
        'Grade',
        back_populates='student',
        cascade='all, delete-orphan'
    )

    def __repr__(self) -> str:
        return f"Student(id={self.id}, name='{self.name}')"


class Group(Base):
    __tablename__ = 'groups'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    students: Mapped[list[Student]] = relationship(
        'Student',
        back_populates='group'
    )

    def __repr__(self) -> str:
        return f"Group(id={self.id}, name='{self.name}')"


class Teacher(Base):
    __tablename__ = 'teachers'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    subjects: Mapped[list['Subject']] = relationship(
        back_populates='teacher',
        cascade='all, delete-orphan'
    )

    def __repr__(self) -> str:
        return f"Teacher(id={self.id}, name='{self.name}')"


class Subject(Base):
    __tablename__ = 'subjects'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    teacher_id: Mapped[int] = mapped_column(
        ForeignKey('teachers.id', ondelete='CASCADE'))
    teacher: Mapped[Teacher] = relationship(
        'Teacher',
        back_populates='subjects'
    )
    grades: Mapped[list['Grade']] = relationship(
        'Grade',
        back_populates='subject',
        cascade='all, delete-orphan'
    )

    def __repr__(self) -> str:
        return f"Subject(id={self.id}, name='{self.name}', teacher_id={self.teacher_id})"


class Grade(Base):
    __tablename__ = 'grades'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(
        ForeignKey('students.id', ondelete='CASCADE'))
    student: Mapped[Student] = relationship(
        'Student',
        back_populates='grades'
    )
    subject_id: Mapped[int] = mapped_column(
        ForeignKey('subjects.id', ondelete='CASCADE'))
    subject: Mapped[Subject] = relationship(
        'Subject',
        back_populates='grades'
    )
    grade: Mapped[int] = mapped_column(Integer, nullable=False)
    date: Mapped[datetime] = mapped_column(default=func.now(), nullable=False)
