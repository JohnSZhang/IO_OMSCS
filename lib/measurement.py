import numpy as np

class Measurement:
    def __init__(self, experiment):
        self.students = experiment.agents
        self.course = experiment.model

    def get_class_stats(self):
        course = self.course
        stats =  {}
        stats['total_chat'] = course.total_chat
        stats['total_posts'] = course.discussion_post
        stats['steps'] = course.step_count
        return stats

    def get_student_stats(self):
        data = {}
        stats = {}
        names = ['chats_read', 'overload_chats_read', 'contrib_chat', 'posts_read',
                 'overload_posts_read', 'contrib_post']
        for n in names:
            data[n] = []

        for s in self.students:
            for n in names:
                data[n].append(getattr(s, n))

        for n in names:
            stats[n] = np.mean(data[n])

        return stats, data


