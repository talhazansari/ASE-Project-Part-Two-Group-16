from src.domain.events.malfunction_reported import MalfunctionReportedEvent

from src.domain.value_objects.malfunction_status import MalfunctionStatus
from datetime import datetime


class MalfunctionReport:
    def __init__(self, user_id,  station_id, description: str):
        self.user_id = user_id
        self.station_id = station_id
        self.description = description
        self.status = MalfunctionStatus.PENDING  # Default status is PENDING
        self.timestamp = datetime.utcnow()  # Timestamp of when the report was created

    def report_malfunction(self):
        """Submit a malfunction report and trigger the malfunction reported event."""
        self.status = MalfunctionStatus.REPORTED
        event = MalfunctionReportedEvent(
            user_id=self.user_id,
            station_id=self.station_id,
            description=self.description,
            timestamp=self.timestamp
        )
        return event
