class User:
    def __init__(self, user_id, name, email, password):
        self.id = user_id
        self.name = name
        self.email = email
        self.password = password
        self.profile = UserProfile(self)

    def get_profile(self):
        return self.profile