class UserProfile:
    def __init__(self, user):
        self.user = user
        self.feedback_history = []  # Stores the feedback history
        self.malfunction_history = []  # Stores the malfunction reports history

    def add_feedback(self, feedback):
        self.feedback_history.append(feedback)

    def add_malfunction_report(self, malfunction_report):
        self.malfunction_history.append(malfunction_report)
