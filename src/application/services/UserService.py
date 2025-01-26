class UserService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def login(self, email, password):
        user = self.user_repository.get_by_email(email)
        if user and user.password == password:
            return user
        return None