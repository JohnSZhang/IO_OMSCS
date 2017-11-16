from lib.experiment import Experiment
from lib.measurement import Measurement
import matplotlib.pyplot as plt

pops = [50, 100, 150, 200, 300, 350, 400, 450, 500]
probs = [0.0, 0.5]
for p in probs:
    total_contribution = []
    social_contributions = []
    for s in pops:
        # print(s, ' students experiment, join chat prob ', p)
        exp = Experiment(100)
        exp.generate_experiment(student_count=s, join_chat_prob=p)
        exp.run_experiment()
        measurement = Measurement(exp)
        class_stats = measurement.get_class_stats()
        student_stats, student_data = measurement.get_student_stats()


        if p == 0.0:
            label = 'Discussion Board Only Non-Social'
            label2 = 'Discussion Board Only Social'
        else:
            label = 'Discussion Board and Chat Non-Social'
            label2 = 'Discussion Board and Chat Social'

        contribution = student_stats['contrib_post']
        social_contribution = student_stats['contrib_social_chat'] + student_stats['contrib_social_post']
        total_contribution.append(contribution)
        social_contributions.append(social_contribution)

    plt.plot(pops, total_contribution, label=label)
    plt.plot(pops, social_contributions, label=label2)

    plt.title('Average # Contribution Per Student vs Class Size')
    plt.xlabel('Number of Students in Class')
    plt.ylabel('Average # of Contribution')
    plt.legend()

plt.show()
