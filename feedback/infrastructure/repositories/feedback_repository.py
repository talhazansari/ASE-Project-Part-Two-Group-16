class FeedbackRepository:
    def __init__(self):
        self.feedbacks = {}

    def save(self, feedback):
        self.feedbacks[feedback.user_id] = feedback
