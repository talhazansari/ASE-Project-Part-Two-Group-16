from feedback.domain.value_objects.feedback_details import FeedbackDetails


class Feedback:
    def __init__(self, user_id, feedback_details: FeedbackDetails):
        self.user_id = user_id
        self.feedback_details = feedback_details
        self.status = "PENDING"  # Default status

    def approve(self):
        self.status = "APPROVED"
