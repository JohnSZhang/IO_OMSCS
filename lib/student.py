from mesa import Agent
import numpy as np

class Student(Agent):
    def __init__(self, id, model, join_chat_prob = 0.5, chat_prob = 0.5, post_prob = 0.5):
        Agent.__init__(self, id, model)
        self.in_chat = False
        self.in_board = False

        self.chats_read = 0
        self.overload_chats_read = 0
        self.contrib_chat = 0

        self.at_post = 0
        self.posts_read = 0
        self.overload_posts_read = 0
        self.contrib_post = 0

        self.join_chat_prob = join_chat_prob
        self.chat_prob = chat_prob
        self.post_prob = post_prob
        self.post_overload_lim = 50
        self.chat_overload_lim = 25
        self.post_overloaded = False
        self.chat_overloaded = False


    def step(self):
        if np.random.random() < self.join_chat_prob:
            chat_num = self.model.join_chat(self.unique_id)
            if chat_num < self.chat_overload_lim and np.random.random() > self.chat_prob:
                self.model.post_in_chat(self.unique_id)
                self.contrib_chat += 1
            self.in_chat = True

        else:
            cur_post_num = self.model.read_board(self.unique_id)
            self.in_board = True
            new_posts = cur_post_num - self.at_post
            if new_posts > self.post_overload_lim:
                self.post_overloaded = True
                self.overload_posts_read += new_posts
            else:
                self.posts_read += new_posts
            self.at_post = cur_post_num



    def interact(self):
        if self.in_chat:
            chats = self.model.get_chat_interaction(self.unique_id)
            if chats < self.chat_overload_lim:
                self.chats_read += chats
            else:
                self.overload_chats_read += chats

        elif self.in_board:
            if (not self.post_overloaded) and (np.random.rand() > self.post_prob):
                self.contrib_post += 1
                self.model.post_discussion(self.unique_id)
        else:
            raise Exception('student will either be in chat or be in discussion board')

    def finish(self):
        self.in_chat = False
        self.in_board = False
        self.post_overloaded = False
        self.chat_overloaded = False

