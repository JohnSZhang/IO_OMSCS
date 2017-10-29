from mesa import Model

class Course(Model):
    def __init__(self):
        Model.__init__(self)
        self.discussion_post = 0
        self.chat_count = 0
        self.chats = {}
        self.discussions = {}
        self.total_chat = 0
        self.step_count = 0


    def step(self):
        self.chat_count = 0
        self.step_count += 1

    def get_chat_interaction(self, id):
        return self.chat_count

    def join_chat(self, id):
       return self.chat_count

    def post_in_chat(self, id):
        self.chat_count += 1
        self.total_chat += 1
        if not id in self.chats.keys():
            self.chats[id] = 1
        else:
            self.chats[id] += 1

    def read_board(self, id):
        return self.discussion_post

    def post_discussion(self, id):
        self.discussion_post += 1
        if not id in self.discussions.keys():
            self.discussions[id] = 1
        else:
            self.discussions[id] += 1

