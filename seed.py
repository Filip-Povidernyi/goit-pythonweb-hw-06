from connect import session
from models import Student, Group, Teacher, Subject, Grade
from sqlalchemy import text
from faker import Faker
import random


if __name__ == "__main__":

    fake = Faker()

    groups = [Group(name=f"Group {i}") for i in range(1, 4)]
    session.add_all(groups)
    session.commit()

    teachers = [Teacher(name=fake.name()) for _ in range(random.randint(3, 5))]
    session.add_all(teachers)
    session.commit()

    subjects = []
    subject_names = [fake.word().capitalize()
                     for _ in range(20)]  # запас варіантів
    chosen_subjects = random.sample(subject_names, k=random.randint(5, 8))
    for subj_name in chosen_subjects:
        teacher = random.choice(teachers)
        subject = Subject(name=subj_name, teacher=teacher)
        subjects.append(subject)
    session.add_all(subjects)
    session.commit()

    students = []
    for _ in range(random.randint(30, 50)):
        student = Student(
            name=fake.name(),
            group=random.choice(groups)
        )
        students.append(student)
    session.add_all(students)
    session.commit()

    for student in students:
        grades_to_create = random.randint(10, 20)
        for _ in range(grades_to_create):
            subject = random.choice(subjects)
            grade_value = random.randint(60, 100)
            # Рандомна дата
            date = fake.date_time_between(start_date='-180d', end_date='now')
            grade = Grade(
                student=student,
                subject=subject,
                grade=grade_value,
                date=date
            )
            session.add(grade)

    session.commit()
    session.close()
