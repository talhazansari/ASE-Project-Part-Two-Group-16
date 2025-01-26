from src.domain.entities.feedback import Feedback


class FeedbackService:
    def __init__(self, feedback_repository, user_repository):
        self.feedback_repository = feedback_repository
        self.user_repository = user_repository

    def submit_feedback(self, user_id, feedback_details):
        user = self.user_repository.get_by_id(user_id)
        if not user:
            return None

        feedback = Feedback(user_id=user.id, feedback_details=feedback_details)
        self.feedback_repository.save(feedback)
        user.get_profile().add_feedback(feedback)  # Add feedback to user's profile

        return feedback