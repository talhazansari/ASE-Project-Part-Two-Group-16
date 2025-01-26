from src.domain.value_objects.feedback_details import FeedbackDetails


class Feedback:
    def __init__(self, user_id, feedback_details, station_name):
        self.user_id = user_id
        self.feedback_details = feedback_details
        self.station_name = station_name  # New attribute for charging station name

    def __str__(self):
        return f"Feedback from User {self.user_id} for Station {self.station_name}: {self.feedback_details}"