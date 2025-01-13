# from streamlit.runtime.scriptrunner import RerunData
# import pytest
# # from feedback.infrastructure.repositories.user_repository import UserRepository
# # from feedback.infrastructure.repositories.feedback_repository import FeedbackRepository
import pytest

from feedback.infrastructure.repositories.feedback_repository import FeedbackRepository
from feedback.infrastructure.repositories.user_repository import UserRepository


@pytest.fixture
def mock_user_repository(monkeypatch):
    repo = UserRepository()
    monkeypatch.setattr("feedback.infrastructure.repositories.user_repository.UserRepository", lambda: repo)
    return repo

@pytest.fixture
def mock_feedback_repository(monkeypatch):
    repo = FeedbackRepository()
    monkeypatch.setattr("feedback.infrastructure.repositories.feedback_repository.FeedbackRepository", lambda: repo)
    return repo

def test_login_success(mock_user_repository):
    user_repo = mock_user_repository
    user = {'id': '1', 'name': 'Test User', 'email': 'test@example.com', 'password': 'password123'}
    user_repo.save(user)

    # Simulate login
    result = user_repo.get_by_email_and_password('test@example.com', 'password123')
    assert result is not None
    assert result['name'] == 'Test User'

def test_login_failure(mock_user_repository):
    user_repo = mock_user_repository

    # Simulate invalid login
    result = user_repo.get_by_email_and_password('invalid@example.com', 'wrongpassword')
    assert result is None

def test_feedback_submission(mock_feedback_repository):
    feedback_repo = mock_feedback_repository

    feedback = {'user_id': '1', 'feedback_text': 'Great experience!', 'rating': 4, 'status': 'Submitted'}
    feedback_repo.save(feedback)

    # Verify feedback is saved
    retrieved_feedback = feedback_repo.get_by_user_id('1')
    assert len(retrieved_feedback) == 1
    assert retrieved_feedback[0]['feedback_text'] == 'Great experience!'
