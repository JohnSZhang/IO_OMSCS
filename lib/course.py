from mesa import Model

class Course(Model):
    def __init__(self):
        Model.__init__(self)
        self.discussion_post = 0
        self.discussion_social_post = 0

        self.total_chat = 0
        self.total_social_chat = 0

        # counters for current period
        self.chat_count = 0
        self.chat_social_count = 0

        self.step_count = 0

    def step(self):
        self.chat_count = 0
        self.chat_social_count = 0
        self.step_count += 1

    def get_chat_interaction(self, id):
        return self.chat_count, self.chat_social_count

    def join_chat(self, id):
       return self.chat_count, self.chat_social_count

    def post_in_chat(self, id, is_social = False):
        if is_social:
            self.chat_social_count += 1
            self.total_social_chat += 1
        else:
            self.chat_count += 1
            self.total_chat += 1

    def read_board(self, id):
        return self.discussion_post, self.discussion_social_post

    def post_discussion(self, id, is_social = False):
        if is_social:
            self.discussion_social_post += 1
        else:
            self.discussion_post += 1


    def get_total_posts(self):
        return self.discussion_post + self.discussion_social_post + self.total_chat + self.total_social_chat