class MalfunctionReportedEvent:
    def __init__(self, user_id, station_id, description, timestamp):
        self.user_id = user_id
        self.station_id = station_id
        self.description = description
        self.timestamp = timestamp

    def __str__(self):
        return (
            f"MalfunctionReportedEvent: User {self.user_id} reported a malfunction at "
            f"Station {self.station_id} - '{self.description}' on {self.timestamp}"
        )
