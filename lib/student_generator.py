from .student import Student


class Student_Generator:
    def __init__(self, model):
        self.model = model
        self.base_class = Student

    def generate_student(self, id, model, params):
        student = Student(id, model, join_chat_prob = params['join_chat'],
                          chat_prob = params['chat_prob'], post_prob = params['post_prob'])
        return student

    def generate_students(self, model, num, join_chat_prob = 0.5):
        params = {}
        params['join_chat'] = join_chat_prob
        params['chat_prob'] = 0.5
        params['post_prob'] = 0.5
        students = []
        model = model or self.model
        for j in range(num):
            students.append(self.generate_student(j, model, params))

        return students




