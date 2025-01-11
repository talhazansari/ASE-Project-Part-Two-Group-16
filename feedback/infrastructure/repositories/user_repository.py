class UserRepository:
    def __init__(self):
        self.users = {}

    def save(self, user):
        self.users[user.id] = user

    def get_by_id(self, user_id):
        return self.users.get(user_id)

    def get_by_email(self, email):
        for user in self.users.values():
            if user.email == email:
                return user
        return None
