from datetime import datetime

from src.domain.entities.malfunctionreport import MalfunctionReport


class MalfunctionService:
    def __init__(self, malfunction_repository, user_repository, station_repository):
        self.malfunction_repository = malfunction_repository
        self.user_repository = user_repository
        self.station_repository = station_repository

    def report_malfunction(self, user_id, station_id, description):
        # Validate user existence
        user = self.user_repository.get_by_id(user_id)
        if not user:
            return None

        # Validate station existence
        station = self.station_repository.get_by_id(station_id)
        if not station:
            return None

        # Create a new malfunction report
        malfunction_report = MalfunctionReport(
            user_id=user.id,
            station_id=station.id,
            description=description,
            timestamp=datetime.utcnow(),
            status="Reported"  # Initial status
        )

        # Save the malfunction report
        self.malfunction_repository.save(malfunction_report)

        # Optionally, associate the malfunction report with the user's profile
        user.get_profile().add_malfunction_report(malfunction_report)

        return malfunction_report
