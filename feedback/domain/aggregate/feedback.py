# domain/aggregates/feedback.py
from feedback.domain.events.feedback_submitted import FeedbackSubmittedEvent
from feedback.domain.value_objects.feedback_details import FeedbackDetails
from feedback.domain.value_objects.feedback_status import FeedbackStatus


class Feedback:
    def __init__(self, user_id, feedback_details: FeedbackDetails):
        self.user_id = user_id
        self.feedback_details = feedback_details
        self.status = FeedbackStatus.PENDING  # Default status is PENDING

    def submit_feedback(self):
        """Submit feedback and trigger the feedback submitted event."""
        self.status = FeedbackStatus.SUBMITTED
        event = FeedbackSubmittedEvent(self.user_id, self.feedback_details)
        return event
