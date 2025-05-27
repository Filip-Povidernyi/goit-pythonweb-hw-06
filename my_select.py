from connect import session
from models import Student, Group, Teacher, Subject, Grade
from sqlalchemy import select, func, desc


def select_1():

    result = session.execute(
        select(
            Student.name,
            func.round(func.avg(Grade.grade), 2).label("average_grade"),
        )
        .join(Grade, Student.id == Grade.student_id)
        .group_by(Student.id)
        .order_by(desc("average_grade"))
        .limit(5)
    )
    print("\nTop 5 students with the highest average grades:")
    for index, row in enumerate(result):
        print(f"{index+1}.Student: {row[0]}, Average Grade: {row[1]}")


def select_2(subject_name: str = '') -> None:
    if subject_name:
        print(f"\nTop student for {subject_name} subject:")
        subjects = session.execute(select(Subject).where(
            Subject.name == subject_name)).scalars().all()
        if not subjects:
            print(f"No subject found with the name '{subject_name}'.")
            return
    else:
        print("\nTop students for each subject:")
        subjects = session.execute(select(Subject)).scalars().all()

    for subject in subjects:
        result = session.execute(
            select(
                Student.name,
                func.round(func.avg(Grade.grade), 2).label("average_grade"),
            )
            .join(Grade, Student.id == Grade.student_id)
            .where(Grade.subject_id == subject.id)
            .group_by(Student.id)
            .order_by(desc("average_grade"))
            .limit(1)
        )
        name, ave = result.all()[0]
        if ave is not None:
            name = name if name else "No student"
            ave = ave if ave is not None else 0
        else:
            name = "No student"
            ave = 0
        print(
            f"Subject: {subject.name}, Student: {name}, Average Grade by subject: {ave}")


def select_3(subject_name: str = '') -> None:
    if subject_name:
        print(f"\nAverage grade for each group by subject:")
        subjects = session.execute(select(Subject.name).where(
            Subject.name == subject_name)).scalars().all()
        if not subjects:
            print(f"No subject found with the name '{subject_name}'.")
            return
    else:
        print("\nAverage grade for each group by subject:")
        subjects = session.execute(select(Subject.name)).scalars().all()

    for subject in subjects:
        result = session.execute(
            select(
                Group.name.label("group_name"),
                func.round(func.avg(Grade.grade), 2).label("average_grade")
            )
            .join(Student, Student.group_id == Group.id)
            .join(Grade, Grade.student_id == Student.id)
            .join(Subject, Grade.subject_id == Subject.id)
            .where(Subject.name == subject)
            .group_by(Group.id)
            .order_by(Group.name)
        )
        for data in result.all():
            group, average_grade = data
            if not group:
                print(f"Subject: {subject}, No data available")
                continue
            print(
                f"Subject: {subject}, Average grade by {group}: {average_grade}")


def select_4():
    result = session.execute(
        select(
            func.round(func.avg(Grade.grade), 2)
            .label("average_grade"))).scalar_one_or_none()

    print(f"\nAverage grade for all students: {result}")


def select_5(teacher_name: str = '') -> None:
    flag = False
    if teacher_name:
        print(f"\nSubjects taught by {teacher_name}:")
        teachers = session.execute(select(Teacher).where(
            Teacher.name == teacher_name)).scalars().all()
        flag = True
        if not teachers:
            print(f"No teacher found with the name '{teacher_name}'.")
            return
    else:
        print("\nAll subjects taught by teachers:")
        teachers = session.execute(select(Teacher)).scalars().all()

    for index, teacher in enumerate(teachers):
        result = session.execute(
            select(Subject.name)
            .join(Teacher)
            .where(Teacher.id == teacher.id)
        ).scalars().all()

        if flag:
            [print(f"{idx+1}.{sbj}") for idx, sbj in enumerate(result)
             ] if result else print("No subjects")
        else:
            print(f"{index+1}. Teacher: {teacher.name}")
            if result:
                print(f'   {result}')
            else:
                print('   No subjects')


def select_6(group_name: str = "") -> None:
    if group_name:
        print(f"\nStudents in group '{group_name}':")
        groups = session.execute(select(Group).where(
            Group.name == group_name)).scalars().all()
        if not groups:
            print(f"No group found with the name '{group_name}'.")
            return
    else:
        print("\nAll students in each group:")
        groups = session.execute(select(Group)).scalars().all()

    for group in groups:
        result = session.execute(
            select(Student.name)
            .where(Student.group_id == group.id)
            .order_by(Student.name)
        ).scalars().all()

        if result:
            print(f"{group.name}:")
            [print(f'   {idx+1}.{student}')
             for idx, student in enumerate(result)]
        else:
            print(f"{group.name}: No students found")


def select_7(group_name: str, subject_name: str) -> None:

    subject_check = session.execute(
        select(Subject).where(Subject.name == subject_name)
    ).scalars().all()

    students_by_group = session.execute(
        select(Student)
        .join(Group)
        .where(Group.name == group_name)
        .order_by(Student.name)
    ).scalars().all()
    if not students_by_group:
        print(f"Please, check a group name '{group_name}'.")
        return
    if not subject_check:
        print(f"Please, check a subject name '{subject_name}'.")
        return
    for idx, student in enumerate(students_by_group):
        result = session.execute(
            select(Grade)
            .join(Subject)
            .where(Grade.student_id == student.id,
                   Subject.name == subject_name)
        ).scalars().all()
        print(f"\n{idx+1}.Grades for {student.name} in {group_name}:")
        if not result:
            print("No grades found")
            continue
        for grade in result:
            if subject_name and grade.subject.name != subject_name:
                continue
            print(
                f"Subject: {grade.subject.name}, Grade: {grade.grade}, Date: {grade.date}")


def select_8(teacher_name: str) -> None:

    res = session.execute(
        select(func.round(func.avg(Grade.grade), 2).label("average_grade"))
        .join(Subject, Grade.subject_id == Subject.id)
        .join(Teacher, Subject.teacher_id == Teacher.id)
        .where(Teacher.name == teacher_name)
    ).scalar_one_or_none()
    if res:
        print(f"\nTeacher {teacher_name} has average grade: {res}")
    else:
        print(
            f"\nTeacher {teacher_name} not found or hasn`t grades.")


def select_9(student_name: str = "") -> None:
    if not student_name:
        students = session.execute(
            select(Student.name).order_by(Student.name)).scalars().all()
    else:
        students = [student_name]
    for student_name in students:
        result = session.execute(
            select(Subject.name)
            .join(Grade, Subject.id == Grade.subject_id)
            .join(Student, Student.id == Grade.student_id)
            .where(Student.name == student_name)
            .distinct()
        ).scalars().all()

        if result:
            print(f"\n{student_name} visiting courses:")
            print([subject for subject in result])
        else:
            print(
                f"\nStudent {student_name} not found or has not courses.")


def select_10(student_name: str = "", teacher_name: str = "") -> None:
    if not student_name or not teacher_name:
        print("\nPlease provide both student and teacher names.")
        return
    result = session.execute(
        select(Subject.name)
        .join(Grade, Subject.id == Grade.subject_id)
        .join(Student, Grade.student_id == Student.id)
        .join(Teacher, Subject.teacher_id == Teacher.id)
        .where(Student.name == student_name)
        .where(Teacher.name == teacher_name)
        .distinct()
    ).scalars().all()

    if result:
        print(f"\nThose courses {teacher_name} teacheng for {student_name}:")
        print([subject for subject in result])
    else:
        print(
            f"\nNo courses that {teacher_name} teaching for {student_name} or this persons are not exists.")


if __name__ == "__main__":
    select_1()
    select_2("Her")
    select_3("Himself")
    select_4()
    select_5("Cody Bennett")
    select_6("Group 1")
    select_7("Group 1", "Himself")
    select_8("Cody Bennett")
    select_9("Nicholas Hudson")
    select_10("Timothy Williamson", "Cody Bennett")
    session.close()
