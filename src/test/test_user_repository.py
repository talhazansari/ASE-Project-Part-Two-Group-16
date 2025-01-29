import os
from unittest.mock import patch, mock_open

import pytest

from src.infrastrucure.repositories.user_repository import UserRepository


@pytest.fixture
def mock_user_repository():
    """Fixture to create an in-memory UserRepository instance."""
    repo = UserRepository(file_path='test_users.csv')
    return repo


def test_save_user(mock_user_repository):
    """Test that a user is saved correctly."""
    user = {'id': '1', 'name': 'Test User', 'email': 'test@example.com', 'password': 'password123'}

    # Save the user
    mock_user_repository.save(user)

    # Verify the user is added to the in-memory list
    assert len(mock_user_repository.users) == 1
    assert mock_user_repository.users[0]['email'] == 'test@example.com'
    assert mock_user_repository.users[0]['password'] == 'password123'


def test_get_user_by_email_and_password(mock_user_repository):
    """Test that a user can be retrieved by email and password."""
    user = {'id': '1', 'name': 'Test User', 'email': 'test@example.com', 'password': 'password123'}
    mock_user_repository.save(user)

    # Retrieve user by email and password
    retrieved_user = mock_user_repository.get_by_email_and_password('test@example.com', 'password123')

    assert retrieved_user is not None
    assert retrieved_user['id'] == '1'
    assert retrieved_user['name'] == 'Test User'


def test_get_user_by_invalid_email_and_password(mock_user_repository):
    """Test that retrieval fails for invalid email or password."""
    user = {'id': '1', 'name': 'Test User', 'email': 'test@example.com', 'password': 'password123'}
    mock_user_repository.save(user)

    # Try to retrieve with incorrect email
    retrieved_user = mock_user_repository.get_by_email_and_password('invalid@example.com', 'password123')
    assert retrieved_user is None

    # Try to retrieve with incorrect password
    retrieved_user = mock_user_repository.get_by_email_and_password('test@example.com', 'wrongpassword')
    assert retrieved_user is None


def test_load_from_csv(mock_user_repository):
    """Test that users are loaded correctly from the CSV file."""
    # Simulate the CSV file content
    mock_csv_content = "id,name,email,password\n1,Test User,test@example.com,password123\n"

    with patch("builtins.open", mock_open(read_data=mock_csv_content)):
        repo = UserRepository(file_path='test_users.csv')

    # Verify that the user is loaded correctly
    assert len(repo.users) == 1
    assert repo.users[0]['email'] == 'test@example.com'
    assert repo.users[0]['password'] == 'password123'


def test_save_user_to_csv(mock_user_repository):
    """Test that a user is correctly saved to the CSV file."""
    user = {'id': '1', 'name': 'Test User', 'email': 'test@example.com', 'password': 'password123'}

    with patch("builtins.open", mock_open()) as mocked_file:
        mock_user_repository.save(user)
        # Verify that the file is opened in append mode
        mocked_file.assert_called_once_with('test_users.csv', mode='a', newline='')

        # Verify that the CSV writing function is called
        mocked_file().write.assert_called_with('1,Test User,test@example.com,password123\n')


@pytest.fixture
def mock_empty_csv_file():
    """Fixture to create an empty CSV file to be used in tests."""
    with patch("builtins.open", mock_open(read_data="id,name,email,password\n")):
        yield 'test_users.csv'
    # Clean up any leftover test files
    if os.path.exists('test_users.csv'):
        os.remove('test_users.csv')


def test_load_empty_csv(mock_empty_csv_file):
    """Test that an empty CSV file loads correctly."""
    repo = UserRepository(file_path=mock_empty_csv_file)
    assert len(repo.users) == 0







