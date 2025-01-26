import csv
import os


class FeedbackRepository:
    def __init__(self, file_path='feedback.csv'):
        self.file_path = file_path
        self.feedbacks = []
        self._load_from_csv()

    def save(self, feedback):
        """Save a feedback dictionary to the repository and CSV."""
        self.feedbacks.append(feedback)
        self._save_to_csv(feedback)

    def get_by_user_id(self, user_id):
        """Retrieve all feedbacks for a specific user ID."""
        return [fb for fb in self.feedbacks if fb['user_id'] == user_id]

    def _save_to_csv(self, feedback):
        """Append a single feedback entry to the CSV file."""
        file_exists = os.path.isfile(self.file_path)
        with open(self.file_path, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['user_id', 'feedback_text', 'rating', 'status'])
            if not file_exists:
                writer.writeheader()  # Write header if file is being created
            writer.writerow(feedback)

    def _load_from_csv(self):
        """Load all feedbacks from the CSV file into the in-memory list."""
        if not os.path.isfile(self.file_path):
            return
        with open(self.file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.feedbacks.append({
                    'user_id': row['user_id'],
                    'feedback_text': row['feedback_text'],
                    'rating': int(row['rating']),
                    'status': row['status']
                })