from mesa import Agent
import numpy as np

class Student(Agent):
    def __init__(self, id, model, params):
        Agent.__init__(self, id, model)

        student_params= {
            'join_chat_prob': 0.15,
            'join_board_prob': 0.15,
            'post_prob': 0.3,
            'reduced_post_prob': 0.1,
            'chat_social_prob': 0.5,
            'post_social_prob': 0.1,
            'discount': 0.95
        }

        student_params.update(params)

        self.in_chat = False
        self.in_board = False
        self.engaged = False

        self.chats_read = 0
        self.chats_social_read = 0
        self.overload_chats_read = 0
        self.overload_chats_social_read = 0
        self.contrib_chat = 0
        self.contrib_social_chat = 0

        self.at_post = 0
        self.at_social_post = 0
        self.posts_read = 0
        self.posts_social_read = 0
        self.overload_posts_read = 0
        self.overload_posts_social_read = 0
        self.contrib_post = 0
        self.contrib_social_post = 0

        self.join_chat_prob = student_params['join_chat_prob']
        self.join_board_prob = student_params['join_board_prob']
        self.post_prob = student_params['post_prob']
        self.reduced_post_prob = student_params['reduced_post_prob']

        self.chat_social_prob = student_params['chat_social_prob']
        self.post_social_prob = student_params['post_social_prob']
        self.discount = student_params['discount']

        self.post_overload_lim = 50
        self.chat_overload_lim = 50
        self.post_overloaded = False
        self.chat_overloaded = False

    def step(self):
        self.post_overloaded = False
        self.chat_overloaded = False
        self.in_chat = False
        self.in_board = False

        r = np.random.rand()
        # with join chat probability we choose chatroom
        if r < self.join_chat_prob:
            chat_num, social_num = self.model.join_chat(self.unique_id)
            self.in_chat = True

            post_prob = self.post_prob
            if (chat_num + social_num) > self.chat_overload_lim:
                post_prob = self.reduced_post_prob

            if np.random.random() < post_prob:
                if np.random.random() < self.chat_social_prob:
                    self.model.post_in_chat(self.unique_id, is_social = True)
                    self.contrib_social_chat += 1
                else:
                    self.model.post_in_chat(self.unique_id, is_social = False)
                    self.contrib_chat += 1

        # with join board probability we choose chatroom
        elif self.join_chat_prob < r < (self.join_chat_prob + self.join_board_prob):
            cur_post_num, cur_social_num = self.model.read_board(self.unique_id)
            self.in_board = True

            new_posts = (cur_post_num - self.at_post) + (cur_social_num - self.at_social_post)
            if new_posts > self.post_overload_lim:
                self.post_overloaded = True
                self.overload_posts_read += cur_post_num - self.at_post
                self.overload_posts_social_read += cur_social_num - self.at_social_post
            else:
                self.posts_read += cur_post_num - self.at_post
                self.posts_social_read += cur_social_num - self.at_social_post

            self.at_post = cur_post_num
            self.at_social_post = cur_social_num



    def interact(self):
        if self.in_chat:
            chats, social_chats = self.model.get_chat_interaction(self.unique_id)
            if (chats + social_chats) < self.chat_overload_lim:
                self.chats_read += chats
                self.chats_social_read += social_chats
            else:
                self.chat_overloaded = True
                self.overload_chats_read += chats
                self.overload_chats_social_read += social_chats

        elif self.in_board:

            post_prob = self.post_prob
            if self.post_overloaded:
                post_prob = self.reduced_post_prob

            if np.random.rand() < post_prob:
                if np.random.rand() < self.post_social_prob:
                    self.contrib_social_post += 1
                    self.model.post_discussion(self.unique_id, is_social = True)
                else:
                    self.contrib_post += 1
                    self.model.post_discussion(self.unique_id, is_social = False)

    def finish(self):
        if self.chat_overloaded:
            self.join_chat_prob *= self.discount
        elif self.post_overloaded:
            self.join_board_prob *= self.discount
