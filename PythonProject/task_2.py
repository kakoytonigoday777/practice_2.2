def read_lines(students):
    with open(students, 'r', encoding='utf-8') as file:
        return file.readlines()

def student_line(line):
    line = line.strip()
    name_student, grades_student = line.split(':')
    name = name_student.strip()
    grades_str = grades_student.split(',')
    grades = []
    for grade_str in grades_str:
        grade = int(grade_str.strip())
        grades.append(grade)
    return name, grades

def sredniy_ball(grades):
    total = 0
    count = 0
    for grade in grades:
        total += grade
        count += 1
    return total / count if count > 0 else 0

def top_students(students, students_sredneye, porog=4.0):
    with open(students, 'w', encoding='utf-8') as file:
        for name, avg in students_sredneye:
            if avg > porog:
                file.write(f"{name}: {avg:.2f}\n")

def luchshiy_student(students_sredneye):
    max_avg = -1
    top_student = None
    for name, avg in students_sredneye:
        if avg > max_avg:
            max_avg = avg
            top_student = name
    return top_student, max_avg

lines = read_lines('students.txt')
students = []

for line in lines:
    name, grades = student_line(line)
    students.append((name, grades))

students_sredneye = []

for student in students:
    name, grades = student
    avg = sredniy_ball(grades)
    students_sredneye.append((name, avg))

top_students('result.txt', students_sredneye)

top_student, top_avg = luchshiy_student(students_sredneye)
print(f"Студент с наивысшим средним баллом: {top_student} ({top_avg:.2f})")