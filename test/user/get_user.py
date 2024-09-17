from unittest.mock import MagicMock
from app.main import get_user, User  # Replace with your actual import paths

def test_get_user_found():
    # Arrange
    mock_db = MagicMock()
    test_email = "test@example.com"
    
    # Create a mock user object
    mock_user = User(email=test_email)
    mock_db.query().filter().first.return_value = mock_user
    
    # Act
    result = get_user(mock_db, test_email)
    
    # Assert
    assert result == mock_user
    mock_db.query().filter().first.assert_called_once()


def test_get_user_not_found():
    # Arrange
    mock_db = MagicMock()
    test_email = "notfound@example.com"
    
    # No user found case
    mock_db.query().filter().first.return_value = None
    
    # Act
    result = get_user(mock_db, test_email)
    
    # Assert
    assert result is None
    mock_db.query().filter().first.assert_called_once()
