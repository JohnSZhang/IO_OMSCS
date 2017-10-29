from .student_generator import Student_Generator
from .course import Course
from .measurement import Measurement
from mesa.time import StagedActivation

class Experiment:
    def __init__(self, steps):
        self.steps = steps

    def generate_experiment(self, student_count = 10, join_chat_prob = .5):
        self.model = Course()
        gen = Student_Generator(self.model)
        self.agents = gen.generate_students(self.model, student_count, join_chat_prob = join_chat_prob)
        self.schedule = StagedActivation(self.model, stage_list=['step', 'interact', 'finish'])
        self.schedule.agents = self.agents


    def run_experiment(self):
        while self.schedule.steps < self.steps:
            self.schedule.step()
            self.model.step()






