from src.domain.value_objects.station_id import StationId


class MalfunctionReport:
    def __init__(self, user_id, station_id, description, timestamp, status="Reported"):
        self.user_id = user_id
        self.station_id = station_id  # Reference to the charging station
        self.description = description  # Details of the malfunction
        self.timestamp = timestamp  # When the malfunction was reported
        self.status = status  # Status of the report (e.g., "Reported", "Resolved")

    def __str__(self):
        return (
            f"Malfunction Report by User {self.user_id} for Station {self.station_id}: "
            f"{self.description} (Status: {self.status}, Reported at: {self.timestamp})"
        )
