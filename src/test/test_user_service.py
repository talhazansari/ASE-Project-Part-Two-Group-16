import pytest
from unittest.mock import MagicMock

from src.application.services.UserService import UserService


@pytest.fixture
def mock_user_repository():
    # Create a mock user repository
    return MagicMock()

def test_login_success(mock_user_repository):
    # Arrange
    email = "test@example.com"
    password = "securepassword"
    user_mock = MagicMock()
    user_mock.password = password
    mock_user_repository.get_by_email.return_value = user_mock

    user_service = UserService(mock_user_repository)

    # Act
    user = user_service.login(email, password)

    # Assert
    assert user is user_mock
    mock_user_repository.get_by_email.assert_called_once_with(email)

def test_login_user_not_found(mock_user_repository):
    # Arrange
    email = "nonexistent@example.com"
    password = "password"
    mock_user_repository.get_by_email.return_value = None

    user_service = UserService(mock_user_repository)

    # Act
    user = user_service.login(email, password)

    # Assert
    assert user is None
    mock_user_repository.get_by_email.assert_called_once_with(email)

def test_login_incorrect_password(mock_user_repository):
    # Arrange
    email = "test@example.com"
    correct_password = "securepassword"
    incorrect_password = "wrongpassword"
    user_mock = MagicMock()
    user_mock.password = correct_password
    mock_user_repository.get_by_email.return_value = user_mock

    user_service = UserService(mock_user_repository)

    # Act
    user = user_service.login(email, incorrect_password)

    # Assert
    assert user is None
    mock_user_repository.get_by_email.assert_called_once_with(email)
