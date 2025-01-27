import pytest
from unittest.mock import patch, MagicMock, mock_open
from datetime import datetime
from io import StringIO
import os

from src.infrastrucure.repositories.malfunction_repository import MalfunctionRepository

@pytest.fixture
def mock_malfunction_repository():
    """Fixture for mocking the MalfunctionRepository class."""
    repo = MalfunctionRepository(file_path='test_malfunctions.csv')
    return repo

def test_save_malfunction(mock_malfunction_repository):
    """Test saving a malfunction report."""
    malfunction_report = {
        'user_id': '1',
        'station_id': 'A123',
        'description': 'Machine overheating',
        'timestamp': datetime.now(),
        'status': 'Open',
        'severity': 2
    }

    mock_malfunction_repository.save(malfunction_report)

    # Verify the malfunction report is saved
    assert len(mock_malfunction_repository.malfunctions) == 1
    saved_report = mock_malfunction_repository.malfunctions[0]
    assert saved_report['user_id'] == '1'
    assert saved_report['station_id'] == 'A123'
    assert saved_report['description'] == 'Machine overheating'
    assert isinstance(saved_report['timestamp'], datetime)
    assert saved_report['status'] == 'Open'
    assert saved_report['severity'] == 2

def test_get_by_user_id(mock_malfunction_repository):
    """Test retrieving malfunction reports by user ID."""
    malfunction_report1 = {
        'user_id': '1',
        'station_id': 'A123',
        'description': 'Machine overheating',
        'timestamp': datetime.now(),
        'status': 'Open',
        'severity': 2
    }
    malfunction_report2 = {
        'user_id': '1',
        'station_id': 'B456',
        'description': 'Power failure',
        'timestamp': datetime.now(),
        'status': 'Closed',
        'severity': 3
    }

    mock_malfunction_repository.save(malfunction_report1)
    mock_malfunction_repository.save(malfunction_report2)

    # Retrieve malfunction reports by user ID
    reports = mock_malfunction_repository.get_by_user_id('1')


    assert reports[0]['user_id'] == '1'
    assert reports[1]['user_id'] == '1'

def test_get_by_station_id(mock_malfunction_repository):
    """Test retrieving malfunction reports by station ID."""
    malfunction_report1 = {
        'user_id': '1',
        'station_id': 'A123',
        'description': 'Machine overheating',
        'timestamp': datetime.now(),
        'status': 'Open',
        'severity': 2
    }
    malfunction_report2 = {
        'user_id': '2',
        'station_id': 'A123',
        'description': 'Power failure',
        'timestamp': datetime.now(),
        'status': 'Closed',
        'severity': 3
    }

    mock_malfunction_repository.save(malfunction_report1)
    mock_malfunction_repository.save(malfunction_report2)

    # Retrieve malfunction reports by station ID
    reports = mock_malfunction_repository.get_by_station_id('A123')


    assert reports[0]['station_id'] == 'A123'
    assert reports[1]['station_id'] == 'A123'


def test_save_to_csv(mock_malfunction_repository):
    """Test that the malfunction report is correctly saved to the CSV file."""
    malfunction_report = {
        'user_id': '1',
        'station_id': 'A123',
        'description': 'Machine overheating',
        'timestamp': datetime.now(),
        'status': 'Open',
        'severity': 2
    }

    # Format timestamp to match the actual format with space between date and time
    timestamp_str = malfunction_report['timestamp'].strftime('%Y-%m-%d %H:%M:%S.%f')

    with patch("builtins.open", mock_open()) as mocked_file:
        mock_malfunction_repository.save(malfunction_report)

        # Verify that the file is opened in append mode
        mocked_file.assert_called_once_with('test_malfunctions.csv', mode='a', newline='')

        # Verify that the CSV writing function is called with the correct values
        expected_line = f"1,A123,Machine overheating,{timestamp_str},Open,2\n"

        # Normalize newlines to account for platform-specific differences.
        actual_call_args = mocked_file().write.call_args[0][0].replace('\r\n', '\n')

        # Check for exact match of the formatted line
        assert actual_call_args == expected_line, f"Expected: {expected_line}, but got: {actual_call_args}"

def test_load_from_csv(mock_malfunction_repository):
    """Test loading malfunction reports from CSV."""
    malfunction_report = {
        'user_id': '1',
        'station_id': 'A123',
        'description': 'Machine overheating',
        'timestamp': datetime.now(),
        'status': 'Open',
        'severity': 2
    }

    # Save a malfunction report to simulate a previous entry
    mock_malfunction_repository.save(malfunction_report)

    # Simulate reading from a file by checking that malfunctions are loaded
    repo = MalfunctionRepository(file_path='test_malfunctions.csv')
    assert len(repo.malfunctions) > 0
    assert repo.malfunctions[0]['user_id'] == '1'

