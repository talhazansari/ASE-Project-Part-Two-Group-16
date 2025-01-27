class MalfunctionDetails:
    def __init__(self, description: str, severity: int):
        """
        Initialize MalfunctionDetails.

        :param description: A description of the malfunction (e.g., "Charger not working").
        :param severity: An integer indicating the severity level of the malfunction (e.g., 1 for minor, 5 for critical).
        """
        self.description = description
        self.severity = severity

    def __str__(self):
        return f"MalfunctionDetails(Description: '{self.description}', Severity: {self.severity})"
