import pytest
from unittest.mock import MagicMock
from datetime import datetime

from src.application.services.MalfunctionService import MalfunctionService


class TestMalfunctionService:

    @pytest.fixture
    def setup(self):
        # Mocking repositories
        malfunction_repository = MagicMock()
        user_repository = MagicMock()

        # Creating the service instance with mocked repositories
        service = MalfunctionService(
            malfunction_repository,
            user_repository,
            None  # Station repository is not required for this test
        )

        return service, malfunction_repository, user_repository

    def test_report_malfunction_success(self, setup):
        service, malfunction_repository, user_repository = setup

        # Mocking a valid user and their profile
        user = MagicMock()
        user.id = 1
        user.get_profile.return_value = MagicMock()  # Mock the user's profile

        # Mocking repository return values
        user_repository.get_by_id.return_value = user

        # Calling the report_malfunction method
        malfunction_report = service.report_malfunction(user.id, 1, "Test malfunction")

        # Assertions
        assert malfunction_report is not None
        assert malfunction_report.user_id == user.id
        assert malfunction_report.description == "Test malfunction"
        assert malfunction_report.status == "Reported"
        assert isinstance(malfunction_report.timestamp, datetime)

        # Verifying repository interactions
        malfunction_repository.save.assert_called_once_with(malfunction_report)
        user.get_profile().add_malfunction_report.assert_called_once_with(malfunction_report)

    def test_report_malfunction_user_not_found(self, setup):
        service, malfunction_repository, user_repository = setup

        # Mocking user not found
        user_repository.get_by_id.return_value = None

        # Calling the report_malfunction method
        malfunction_report = service.report_malfunction(1, 1, "Test malfunction")

        # Assertions
        assert malfunction_report is None
        user_repository.get_by_id.assert_called_once_with(1)

    def test_report_malfunction_station_not_needed(self, setup):
        service, malfunction_repository, user_repository = setup

        # Mocking a valid user, but no need for station
        user = MagicMock()
        user.id = 1
        user_repository.get_by_id.return_value = user

        # Calling the report_malfunction method
        malfunction_report = service.report_malfunction(user.id, None, "Test malfunction")

        # Assertions
        assert malfunction_report is not None
        user_repository.get_by_id.assert_called_once_with(user.id)

    def test_report_malfunction_user_and_station_not_found(self, setup):
        service, malfunction_repository, user_repository = setup

        # Mocking user not found
        user_repository.get_by_id.return_value = None

        # Calling the report_malfunction method
        malfunction_report = service.report_malfunction(1, 1, "Test malfunction")

        # Assertions
        assert malfunction_report is None
        user_repository.get_by_id.assert_called_once_with(1)
