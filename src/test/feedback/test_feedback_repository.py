import os

import pytest
from unittest.mock import mock_open, patch

from src.infrastrucure.repositories.feedback_repository import FeedbackRepository


@pytest.fixture
def mock_feedback_repository():
    """Fixture to create an in-memory FeedbackRepository instance."""
    repo = FeedbackRepository(file_path='test_feedback.csv')
    return repo


def test_save_feedback(mock_feedback_repository):
    """Test that feedback is saved correctly."""
    feedback = {'user_id': '1', 'feedback_text': 'Great experience!', 'rating': 4, 'station_name': 'Station A',
                'status': 'Submitted'}

    # Save the feedback
    mock_feedback_repository.save(feedback)

    # Verify the feedback is added to the in-memory list
    assert len(mock_feedback_repository.feedbacks) == 1
    assert mock_feedback_repository.feedbacks[0]['feedback_text'] == 'Great experience!'
    assert mock_feedback_repository.feedbacks[0]['rating'] == 4


def test_get_feedback_by_user_id(mock_feedback_repository):
    """Test that feedback can be retrieved by user ID."""
    feedback1 = {'user_id': '1', 'feedback_text': 'Great experience!', 'rating': 4, 'station_name': 'Station A',
                 'status': 'Submitted'}
    feedback2 = {'user_id': '2', 'feedback_text': 'Good service', 'rating': 3, 'station_name': 'Station B',
                 'status': 'Submitted'}
    mock_feedback_repository.save(feedback1)
    mock_feedback_repository.save(feedback2)

    # Retrieve feedback by user ID
    retrieved_feedback = mock_feedback_repository.get_by_user_id('1')


    assert retrieved_feedback[0]['user_id'] == '1'
    assert retrieved_feedback[0]['feedback_text'] == 'Great experience!'


def test_get_feedback_by_non_existent_user_id(mock_feedback_repository):
    """Test that retrieving feedback for a non-existent user ID returns an empty list."""
    feedback1 = {'user_id': '1', 'feedback_text': 'Great experience!', 'rating': 4, 'station_name': 'Station A',
                 'status': 'Submitted'}
    mock_feedback_repository.save(feedback1)

    # Try to retrieve feedback for a non-existent user ID
    retrieved_feedback = mock_feedback_repository.get_by_user_id('999')
    assert len(retrieved_feedback) == 0


def test_load_from_csv(mock_feedback_repository):
    """Test that feedbacks are loaded correctly from the CSV file."""
    # Simulate the CSV file content
    mock_csv_content = "user_id,feedback_text,rating,station_name,status\n1,Great experience!,4,Station A,Submitted\n2,Good service,3,Station B,Submitted\n"

    with patch("builtins.open", mock_open(read_data=mock_csv_content)):
        repo = FeedbackRepository(file_path='test_feedback.csv')

    # Verify that feedbacks are loaded correctly
    assert len(repo.feedbacks) == 2
    assert repo.feedbacks[0]['user_id'] == '1'
    assert repo.feedbacks[1]['station_name'] == 'Station B'


def test_save_feedback_to_csv(mock_feedback_repository):
    """Test that feedback is correctly saved to the CSV file."""
    feedback = {'user_id': '1', 'feedback_text': 'Great experience!', 'rating': 4, 'station_name': 'Station A',
                'status': 'Submitted'}

    with patch("builtins.open", mock_open()) as mocked_file:
        mock_feedback_repository.save(feedback)

        # Verify that the file is opened in append mode
        mocked_file.assert_called_once_with('test_feedback.csv', mode='a', newline='')

        # Verify that the CSV writing function is called with the correct line endings
        mocked_file().write.assert_called_with('1,Great experience!,4,Station A,Submitted\r\n')  # Adjusted expected value


@pytest.fixture
def mock_empty_csv_file():
    """Fixture to create an empty CSV file to be used in tests."""
    with patch("builtins.open", mock_open(read_data="user_id,feedback_text,rating,station_name,status\n")):
        yield 'test_feedback.csv'
    # Clean up any leftover test files
    if os.path.exists('test_feedback.csv'):
        os.remove('test_feedback.csv')


def test_load_empty_csv(mock_empty_csv_file):
    """Test that an empty CSV file loads correctly."""
    repo = FeedbackRepository(file_path=mock_empty_csv_file)
    assert len(repo.feedbacks) == 0
