import csv
import os
from datetime import datetime

class MalfunctionRepository:
    def __init__(self, file_path='malfunctions.csv'):
        self.file_path = file_path
        self.malfunctions = []
        self._load_from_csv()

    def save(self, malfunction_report):
        """Save a malfunction report dictionary to the repository and CSV."""
        report_data = {
            'user_id': malfunction_report['user_id'],  # Accessing 'user_id' as a key in the dictionary
            'station_id': malfunction_report['station_id'],
            'description': malfunction_report['description'],
            'timestamp': malfunction_report['timestamp'],
            'status': malfunction_report['status'],
            'severity': malfunction_report['severity']  # Including severity
        }
        self.malfunctions.append(report_data)
        self._save_to_csv(report_data)

    def get_by_user_id(self, user_id):
        """Retrieve all malfunction reports for a specific user ID."""
        return [mr for mr in self.malfunctions if mr['user_id'] == user_id]

    def get_all_malfunctions(self):
        return [mr for mr in self.malfunctions]




    def get_by_station_id(self, station_id):
        """Retrieve all malfunction reports for a specific station ID."""
        return [mr for mr in self.malfunctions if mr['station_id'] == station_id]

    def _save_to_csv(self, malfunction_report):
        """Append a single malfunction report entry to the CSV file."""
        file_exists = os.path.isfile(self.file_path)
        with open(self.file_path, mode='a', newline='') as file:
            writer = csv.DictWriter(
                file,
                fieldnames=['user_id', 'station_id', 'description', 'timestamp', 'status', 'severity']  # Include 'severity'
            )
            if not file_exists:
                writer.writeheader()  # Write header if file is being created
            writer.writerow(malfunction_report)

    def _load_from_csv(self):
        """Load all malfunction reports from the CSV file into the in-memory list."""
        if not os.path.isfile(self.file_path):
            return
        with open(self.file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.malfunctions.append({
                    'user_id': row['user_id'],
                    'station_id': row['station_id'],
                    'description': row['description'],
                    'timestamp': datetime.fromisoformat(row['timestamp']),
                    'status': row['status'],
                    'severity': int(row['severity'])  # Make sure to load severity as an integer
                })
