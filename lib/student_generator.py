from .student import Student


class Student_Generator:
    def __init__(self, model, student_params):
        self.model = model
        self.base_class = Student
        self.student_params = student_params

    def generate_students(self, model, num):
        students = []
        model = model or self.model
        for j in range(num):
            student = Student(j, model, self.student_params)
            students.append(student)

        return students




