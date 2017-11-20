from lib.experiment import Experiment
import matplotlib.pyplot as plt
import pandas as pd
from mesa.datacollection import DataCollector

# pops = [50, 100, 150, 200, 300, 350, 400, 450, 500]
pops = [50, 100, 200, 300, 500, 1000]
probs = [0.0]


for p in probs:
    total_contribution = []
    social_contributions = []
    for s in pops:
        print(s, ' students experiment, join chat prob ', p)
        exp = Experiment(100)
        model_reporters = {}
        model_reporters['post_count'] = lambda m: m.get_total_posts()

        def is_overload(a):
            if a.post_overloaded or a.chat_overloaded:
                return 1
            return 0


        def is_engaged(a):
            if a.in_chat or a.in_board:
                return 1
            return 0

        agent_reporters = {}
        agent_reporters['overload_count'] = is_overload
        agent_reporters['engagement_count'] = is_engaged
        data_collector = DataCollector(model_reporters = model_reporters, agent_reporters=agent_reporters)

        experiment_params = {
            'join_board_prob': 0.30,
            'join_chat_prob': 0.0
        }
        exp.setup_experiment(student_count=s, student_params = experiment_params, data_collector = data_collector)
        exp.run_experiment()

        model_data = exp.data_collector.get_model_vars_dataframe()
        agent_data = exp.data_collector.get_agent_vars_dataframe()

        overload_count = agent_data['overload_count']
        overload_by_step = overload_count.sum(level="Step")
        engagement_count = agent_data['engagement_count']
        engagement_by_step = engagement_count.sum(level="Step")

        posts = model_data['post_count'].diff()
        avg = pd.rolling_mean(posts, 15)
        plt.plot(posts)
        plt.plot(overload_by_step)
        plt.plot(engagement_by_step)
        plt.legend()
        plt.title('Number of New Post Per Period Vs Overloaded Students Count')
        plt.xlabel('Step')
        plt.ylabel('Number of Items')
        plt.legend()
        plt.savefig('data/' + str(s) + ' students-posts-over-time.png')
        plt.clf()

