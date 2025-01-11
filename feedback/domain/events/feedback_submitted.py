class FeedbackSubmittedEvent:
    def __init__(self, user_id, feedback_details):
        self.user_id = user_id
        self.feedback_details = feedback_details