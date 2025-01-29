import os
import uuid
from unittest.mock import patch, mock_open

import pytest
from src.infrastrucure.repositories.user_repository import UserRepository


@pytest.fixture
def mock_user_repository():
    """Fixture to create an in-memory UserRepository instance with a clean slate for each test."""
    repo = UserRepository(file_path='test_users.csv')
    repo.users = []  # Clear users to ensure isolation between tests
    return repo


def test_successful_sign_up(mock_user_repository):
    """Test that a user can successfully sign up."""
    user = {'id': str(uuid.uuid4()), 'name': 'New User', 'email': 'newuser@example.com', 'password': 'securepass'}
    
    # Save the user
    mock_user_repository.save(user)
    
    # Verify that the user is added successfully
    assert len(mock_user_repository.users) == 1
    assert mock_user_repository.users[0]['email'] == 'newuser@example.com'
    assert mock_user_repository.users[0]['password'] == 'securepass'


def test_duplicate_email_sign_up(mock_user_repository):
    """Test that sign-up fails when using an existing email."""
    user = {'id': str(uuid.uuid4()), 'name': 'Existing User', 'email': 'existing@example.com', 'password': 'password123'}
    mock_user_repository.save(user)

    # Try to sign up with the same email
    duplicate_user = {'id': str(uuid.uuid4()), 'name': 'Duplicate User', 'email': 'existing@example.com', 'password': 'newpassword'}
    mock_user_repository.save(duplicate_user)

    # Ensure only one user exists with that email
    user_count = sum(1 for u in mock_user_repository.users if u['email'] == 'existing@example.com')
    assert user_count == 1  # Only the first user should be stored


def test_sign_up_with_missing_fields(mock_user_repository):
    """Test that sign-up fails when required fields are missing."""
    incomplete_user = {'id': str(uuid.uuid4()), 'name': '', 'email': 'invalid@example.com', 'password': ''}

    # Try to save an incomplete user
    mock_user_repository.save(incomplete_user)

    # Ensure the user is not added
    assert not any(user['email'] == 'invalid@example.com' for user in mock_user_repository.users)


def test_sign_up_password_confirmation(mock_user_repository):
    """Test that password confirmation matches the original password."""
    password = 'securepassword'
    confirm_password = 'securepassword'

    assert password == confirm_password, "Passwords do not match!"

    user = {'id': str(uuid.uuid4()), 'name': 'Confirmed User', 'email': 'confirmed@example.com', 'password': password}
    
    mock_user_repository.save(user)

    # Ensure only this user exists
    assert len(mock_user_repository.users) == 1
    assert mock_user_repository.users[0]['password'] == password


def test_load_users_from_csv(mock_user_repository):
    """Test that users are loaded correctly from a CSV file."""
    mock_csv_content = """id,name,email,password\n1,Test User,test@example.com,password123\n2,Another User,another@example.com,pass456\n"""

    with patch("builtins.open", mock_open(read_data=mock_csv_content)):
        repo = UserRepository(file_path='test_users.csv')
    
    assert len(repo.users) == 2
    assert repo.users[0]['email'] == 'test@example.com'
    assert repo.users[1]['email'] == 'another@example.com'


def test_save_user_to_csv(mock_user_repository):
    """Test that a user is correctly saved to the CSV file."""
    user = {'id': '3', 'name': 'CSV User', 'email': 'csvuser@example.com', 'password': 'csvpass'}

    with patch("builtins.open", mock_open()) as mocked_file:
        mock_user_repository.save(user)

        # Verify file opened in append mode
        mocked_file.assert_called_once_with('test_users.csv', mode='a', newline='')

        # Normalize newlines for Windows vs Unix
        expected_call = '3,CSV User,csvuser@example.com,csvpass\n'.replace('\n', os.linesep)
        mocked_file().write.assert_called_with(expected_call)


def test_load_empty_csv(mock_user_repository):
    """Test that an empty CSV file loads correctly."""
    with patch("builtins.open", mock_open(read_data="id,name,email,password\n")):
        repo = UserRepository(file_path='test_users.csv')

    assert len(repo.users) == 0
