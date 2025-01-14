class UserProfile:
    def __init__(self, user):
        self.user = user
        self.feedback_history = []  # Stores the feedback history

    def add_feedback(self, feedback):
        self.feedback_history.append(feedback)
