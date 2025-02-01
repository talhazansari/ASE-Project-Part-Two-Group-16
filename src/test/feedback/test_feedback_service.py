import pytest
from unittest.mock import MagicMock

from src.application.services.FeedbackService import FeedbackService


@pytest.fixture
def mock_repositories():
    user_repo = MagicMock()
    feedback_repo = MagicMock()
    return user_repo, feedback_repo

def test_submit_feedback(mock_repositories):
    user_repo, feedback_repo = mock_repositories
    user_mock = MagicMock(id=1)
    profile_mock = MagicMock()
    user_mock.get_profile.return_value = profile_mock
    profile_mock.add_feedback = MagicMock()
    user_repo.get_by_id.return_value = user_mock

    feedback_service = FeedbackService(feedback_repo, user_repo)

    feedback_details = "Great service!"
    station_name = "Station A"
    user_id = 1

    feedback = feedback_service.submit_feedback(user_id, feedback_details, station_name)

    assert feedback is not None
    user_repo.get_by_id.assert_called_once_with(user_id)
    feedback_repo.save.assert_called_once()
    profile_mock.add_feedback.assert_called_once()
