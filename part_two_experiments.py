from lib.experiment import Experiment
import matplotlib.pyplot as plt
from mesa.datacollection import DataCollector
num_steps = 100
pops = [25, 50, 100, 150, 200, 300, 350, 400, 450, 500]
probs = [(0.3, 0.0), (0.15, 0.15)]
data = {
    'single-attn-social': [],
    'single-attn-course': [],
    'dual-attn-social': [],
    'dual-attn-course': [],
    'single-contri-social': [],
    'dual-contri-social': [],
    'single-contri-course': [],
    'dual-contri-course': []
    }
for p in probs:
    total_posts = []
    for s in pops:
        print(s, ' students experiment, join chat prob ', p)
        a, b = p
        exp = Experiment(num_steps)

        def non_overload_course(a):
            return a.posts_read + a.chats_read

        def non_overload_social(a):
            return a.posts_social_read + a.chats_social_read

        def course_contributions_made(a):
            return a.contrib_post + a.contrib_chat

        def social_contributions_made(a):
            return a.contrib_social_post + a.contrib_social_chat

        agent_reporters = {}
        agent_reporters['non_overload_course'] = non_overload_course
        agent_reporters['non_overload_social'] = non_overload_social
        agent_reporters['contribution_course'] = course_contributions_made
        agent_reporters['contribution_social'] = social_contributions_made


        data_collector = DataCollector(agent_reporters=agent_reporters)

        experiment_params = {
            'join_board_prob': a,
            'join_chat_prob': b
        }
        exp.setup_experiment(student_count=s, data_collector = data_collector, student_params = experiment_params)
        exp.run_experiment()

        agent_data = exp.data_collector.get_agent_vars_dataframe()

        def last_step_avg(frame):
            last_step_val = frame[num_steps-1]
            return last_step_val.mean()

        total_read_course = last_step_avg(agent_data['non_overload_course'])
        total_read_social = last_step_avg(agent_data['non_overload_social'])
        total_contri_course = last_step_avg(agent_data['contribution_course'])
        total_contri_social = last_step_avg(agent_data['contribution_social'])

        if a == 0.30:
            prefix = 'single'
        else:
            prefix = 'dual'

        data[prefix+'-attn-social'].append(total_read_social)
        data[prefix+'-attn-course'].append(total_read_course)
        data[prefix+'-contri-social'].append(total_contri_social)
        data[prefix+'-contri-course'].append(total_contri_course)


plt.plot(pops, data['single-attn-social'], label='single channel social items')
plt.plot(pops, data['dual-attn-social'], label='two channels social items')
plt.plot(pops, data['single-attn-course'], label='single channels course items')
plt.plot(pops, data['dual-attn-course'], label='two channels course items')
plt.title('Average Total Items Read Per Student vs Class Size')
plt.xlabel('Number of Students in Class')
plt.ylabel('Number of Posts Read')
plt.legend()
plt.savefig('data/' + 'items-read-v-size.png')
plt.clf()

plt.plot(pops, data['single-contri-social'], label='single channel social items')
plt.plot(pops, data['dual-contri-social'], label='two channels social items')
plt.plot(pops, data['single-contri-course'], label='single channels course items')
plt.plot(pops, data['dual-contri-course'], label='two channels course items')
plt.title('Average Total Items Contributed Per Student vs Class Size')
plt.xlabel('Number of Students in Class')
plt.ylabel('Number of Posts Contributed')
plt.legend()
plt.savefig('data/' + 'items-contributed-v-size.png')
plt.clf()

