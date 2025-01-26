# class UserRepository:
#     def __init__(self):
#         self.users = {}

#     def save(self, user):
#         self.users[user.id] = user

#     def get_by_id(self, user_id):
#         return self.users.get(user_id)

#     def get_by_email(self, email):
#         for user in self.users.values():
#             if user.email == email:
#                 return user
#         return None


import csv
import os


class UserRepository:
    def __init__(self, file_path='users.csv'):
        self.file_path = file_path
        self.users = []
        self._load_from_csv()

    def save(self, user):
        """Save a user dictionary to the repository and CSV."""
        self.users.append(user)
        self._save_to_csv(user)

    def get_by_email_and_password(self, email, password):
        """Retrieve a user by email and password."""
        for user in self.users:
            if user['email'] == email and user['password'] == password:
                return user
        return None

    def _save_to_csv(self, user):
        """Append a single user entry to the CSV file."""
        file_exists = os.path.isfile(self.file_path)
        with open(self.file_path, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['id', 'name', 'email', 'password'])
            if not file_exists:
                writer.writeheader()  # Write header if file is being created
            writer.writerow(user)

    def _load_from_csv(self):
        """Load all users from the CSV file into the in-memory list."""
        if not os.path.isfile(self.file_path):
            return
        with open(self.file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.users.append({
                    'id': row['id'],
                    'name': row['name'],
                    'email': row['email'],
                    'password': row['password']
                })