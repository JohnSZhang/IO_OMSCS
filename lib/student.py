from mesa import Agent
import numpy as np

class Student(Agent):
    def __init__(self, id, model, engage_prob = 0.3, join_chat_prob = 0.5, chat_prob = 0.5, post_prob = 0.5,
                 chat_social_prob = 0.5, post_social_prob =0.1):
        Agent.__init__(self, id, model)
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

        self.join_chat_prob = join_chat_prob
        self.chat_prob = chat_prob
        self.post_prob = post_prob
        self.chat_social_prob = chat_social_prob
        self.post_social_prob = post_social_prob
        self.engage_prob = engage_prob
        self.post_overload_lim = 50
        self.chat_overload_lim = 50
        self.post_overloaded = False
        self.chat_overloaded = False


    def step(self):
        if np.random.rand() < self.engage_prob:
            self.engaged = True
            if np.random.random() < self.join_chat_prob:
                chat_num, social_num = self.model.join_chat(self.unique_id)
                if chat_num + social_num < self.chat_overload_lim and np.random.random() > self.chat_prob:
                    if np.random.random() < self.chat_social_prob:
                        self.model.post_in_chat(self.unique_id, is_social = True)
                        self.contrib_social_chat += 1
                    else:
                        self.model.post_in_chat(self.unique_id, is_social = False)
                        self.contrib_chat += 1
                self.in_chat = True

            else:
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
        if self.in_chat and self.engaged:
            chats, social_chats = self.model.get_chat_interaction(self.unique_id)
            if (chats + social_chats) < self.chat_overload_lim:
                self.chats_read += chats
                self.chats_social_read += social_chats
            else:
                self.overload_chats_read += chats
                self.overload_chats_social_read += social_chats

        elif self.in_board and self.engaged:
            if (not self.post_overloaded) and (np.random.rand() > self.post_prob):
                if np.random.rand() < self.post_social_prob:
                    self.contrib_social_post += 1
                    self.model.post_discussion(self.unique_id, is_social = True)
                else:
                    self.contrib_post += 1
                    self.model.post_discussion(self.unique_id, is_social = False)

    def finish(self):
        self.in_chat = False
        self.in_board = False
        self.post_overloaded = False
        self.chat_overloaded = False
        self.engaged = False

