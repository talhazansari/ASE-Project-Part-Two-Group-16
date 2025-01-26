class Session:
    def __init__(self):
        self.logged_in_user = None

    def login(self, user):
        self.logged_in_user = user

    def logout(self):
        self.logged_in_user = None

    def get_logged_in_user(self):
        return self.logged_in_user