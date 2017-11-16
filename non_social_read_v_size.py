from lib.experiment import Experiment
from lib.measurement import Measurement
import matplotlib.pyplot as plt

pops = [50, 100, 150, 200, 300, 350, 400, 450, 500]
probs = [0.0, 0.5]
for p in probs:
    total_posts = []

    for s in pops:
        # print(s, ' students experiment, join chat prob ', p)
        exp = Experiment(100)
        exp.generate_experiment(student_count=s, join_chat_prob=p)
        exp.run_experiment()
        measurement = Measurement(exp)
        class_stats = measurement.get_class_stats()
        student_stats, student_data = measurement.get_student_stats()

        total_social_posts_read = student_stats['chats_social_read'] + student_stats['posts_social_read']

        total_not_overloaded_posts_read = student_stats['posts_read'] + student_stats['chats_read']

        total_overloaded_posts_read = student_stats['overload_chats_read'] + student_stats['overload_posts_read']
        # print('total posts read', total_not_overloaded_posts_read)
        # print('total social posts read', total_not_overloaded_posts_read)

        if p == 0.0:
            label = 'Discussion Board Only'
        else:
            label = 'Discussion Board and Chat'

        total_posts.append(total_not_overloaded_posts_read + total_overloaded_posts_read)
    plt.plot(pops, total_posts, label=label)
    plt.title('Average Total Items Read Per Student vs Class Size')
    plt.xlabel('Number of Students in Class')
    plt.ylabel('Number of Total Items Read')
    plt.legend()

plt.show()

