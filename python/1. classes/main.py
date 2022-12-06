class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_lecture(self, lecturer, course, grade):
        if isinstance(lecturer, Lecturer) and course in lecturer.courses_attached \
                and course in self.courses_in_progress:
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'

    def avg_grade(self):
        if self.grades.values():
            return sum(sum(self.grades.values(), [])) / len(sum(self.grades.values(), []))
        else:
            return 0

    def __str__(self):
        return (f'Имя: {self.name}\n'
                f'Фамилия: {self.surname}\n'
                f'Средняя оценка за домашнее задание: {self.avg_grade():.2f}\n'
                f'Курсы в процессе изучения: {", ".join(self.courses_in_progress)}\n'
                f'Завершенные курсы: {", ".join(self.finished_courses)}\n')

    def __lt__(self, other):
        if self.avg_grade() < other.avg_grade():
            return True
        else:
            return False


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

    def __str__(self):
        return (f'Имя: {self.name}\n'
                f'Фамилия: {self.surname}\n')


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def avg_grade(self):
        if self.grades.values():
            return sum(sum(self.grades.values(), [])) / len(sum(self.grades.values(), []))
        else:
            return 0

    def __str__(self):
        return super().__str__() + f'Средняя оценка за лекции: {self.avg_grade():.2f}\n'

    def __lt__(self, other):
        if isinstance(other, type(self)):
            if self.avg_grade() < other.avg_grade():
                return True
            else:
                return False


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'


def avg_lecture_grade(course, lecturers):
    grade_list = sum((lecturer.grades[course] for lecturer in lecturers if isinstance(lecturer, Lecturer)
                      and course in lecturer.grades), [])
    if grade_list:
        return sum(grade_list) / len(grade_list)
    else:
        return 0


def avg_hw_grade(course, students):
    grade_list = sum((student.grades[course] for student in students if isinstance(student, Student)
                      and course in student.grades), [])
    if grade_list:
        return sum(grade_list) / len(grade_list)
    else:
        return 0


best_student = Student('Ruoy', 'Eman', 'your_gender')
best_student.courses_in_progress += ['Python', 'Git']
worst_student = Student('James', 'Moore', 'male')
worst_student.courses_in_progress += ['Python']

cool_reviewer = Reviewer('Some', 'Buddy')
cool_reviewer.courses_attached += ['Python', 'Git']
warm_reviewer = Reviewer('Annie', 'Buddy')
warm_reviewer.courses_attached += ['Python', 'Git']

smart_lecturer = Lecturer('Hannibal', 'Lecter')
smart_lecturer.courses_attached += ['Python', 'Git']
very_smart_lecturer = Lecturer('Walter', 'White')
very_smart_lecturer.courses_attached += ['Python']

best_student.rate_lecture(smart_lecturer, 'Git', 7)
worst_student.rate_lecture(smart_lecturer, 'Python', 8)
best_student.rate_lecture(very_smart_lecturer, 'Python', 10)
worst_student.rate_lecture(very_smart_lecturer, 'Python', 9)

warm_reviewer.rate_hw(best_student, 'Git', 9)
cool_reviewer.rate_hw(best_student, 'Python', 8)
warm_reviewer.rate_hw(worst_student, 'Python', 7)
cool_reviewer.rate_hw(worst_student, 'Python', 6)

print(best_student)
print(worst_student)
print(cool_reviewer)
print(warm_reviewer)
print(smart_lecturer)
print(very_smart_lecturer)

print(max(best_student, worst_student))
print(max(smart_lecturer, very_smart_lecturer))

student_list = [best_student, worst_student]
lecturer_list = [smart_lecturer, very_smart_lecturer]

print(avg_lecture_grade('Python', lecturer_list))
print(avg_lecture_grade('JavaScript', lecturer_list))

print(avg_hw_grade('Python', student_list))
print(avg_hw_grade('Git', student_list))
