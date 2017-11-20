from .student_generator import Student_Generator
from .course import Course
from mesa.time import StagedActivation
from mesa.datacollection import DataCollector

class Experiment:
    def __init__(self, steps):
        self.steps = steps


    def setup_experiment(self, student_count = 10, data_collector = DataCollector(),
                            student_params = {}):
        self.model = Course()
        gen = Student_Generator(self.model, student_params)
        self.agents = gen.generate_students(self.model, student_count)
        self.schedule = StagedActivation(self.model, stage_list=['step', 'interact', 'finish'])
        self.schedule.agents = self.agents
        self.model.schedule = self.schedule
        self.data_collector = data_collector

    def run_experiment(self):
        while self.schedule.steps < self.steps:
            self.schedule.step()
            self.model.step()
            self.data_collector.collect(self.model)








