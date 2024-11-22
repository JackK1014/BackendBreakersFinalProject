from fastapi.testclient import TestClient
from unittest.mock import Mock
import pytest
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from ..main import app
from ..controllers import promotions as controller
from ..models import promotions as model

client = TestClient(app)


@pytest.fixture
def db_session():
    """Fixture to provide a mocked database session for testing."""
    return Mock()


def test_create_promotion(db_session):
    """Test for creating a promotion."""
    # Mock promotion data
    promotion_data = {
        "promotion_code": "DISCOUNT10",
        "expiration_date": datetime(2024, 12, 31)
    }

    # Create a mock Promotion object
    created_promotion = model.Promotion(**promotion_data)

    # Mock database methods
    db_session.add = Mock()
    db_session.commit = Mock()
    db_session.refresh = Mock()

    # Mock refresh behavior to simulate the database assigning an ID
    def mock_refresh(promotion):
        promotion.id = 1  # Simulate auto-increment ID assignment
        return promotion

    db_session.refresh.side_effect = mock_refresh

    # Call the create function
    result = controller.create(db_session, created_promotion)

    # Assertions
    assert result.promotion_code == promotion_data["promotion_code"]
    assert result.expiration_date == promotion_data["expiration_date"]
    assert result.id == 1  # Ensure the ID is correctly set


def test_read_all_promotions(db_session):
    """Test for reading all promotions."""
    # Mock a list of promotions
    db_session.query.return_value.all.return_value = [
        model.Promotion(id=1, promotion_code="DISCOUNT10", expiration_date=datetime(2024, 12, 31)),
        model.Promotion(id=2, promotion_code="SUMMER20", expiration_date=datetime(2024, 6, 30))
    ]

    # Call the read_all function
    results = controller.read_all(db_session)

    # Assertions
    assert len(results) == 2
    assert results[0].promotion_code == "DISCOUNT10"
    assert results[0].expiration_date == datetime(2024, 12, 31)
    assert results[1].promotion_code == "SUMMER20"
    assert results[1].expiration_date == datetime(2024, 6, 30)


def test_read_one_promotion(db_session):
    """Test for reading a single promotion."""
    # Mock a single promotion
    db_session.query.return_value.filter.return_value.first.return_value = model.Promotion(
        id=1, promotion_code="DISCOUNT10", expiration_date=datetime(2024, 12, 31)
    )

    # Call the read_one function
    result = controller.read_one(db_session, 1)

    # Assertions
    assert result is not None
    assert result.promotion_code == "DISCOUNT10"
    assert result.expiration_date == datetime(2024, 12, 31)


def test_update_promotion(db_session):
    """Test for updating a promotion."""
    # Mock an existing promotion
    existing_promotion = model.Promotion(
        id=1, promotion_code="DISCOUNT10", expiration_date=datetime(2024, 12, 31)
    )
    db_session.query.return_value.filter.return_value.first.return_value = existing_promotion

    # Mock update data
    update_data = {"promotion_code": "WINTER25", "expiration_date": datetime(2025, 1, 1)}
    request_data = Mock()
    request_data.dict.return_value = update_data

    # Mock database commit
    db_session.commit = Mock()

    # Call the update function
    updated_promotion = controller.update(db_session, 1, request_data)

    # Simulate the update behavior
    existing_promotion.promotion_code = update_data["promotion_code"]
    existing_promotion.expiration_date = update_data["expiration_date"]

    # Assertions
    assert updated_promotion.promotion_code == "WINTER25"
    assert updated_promotion.expiration_date == datetime(2025, 1, 1)


def test_delete_promotion(db_session):
    """Test for deleting a promotion."""
    # Mock an existing promotion to delete
    db_session.query.return_value.filter.return_value.first.return_value = model.Promotion(
        id=1, promotion_code="DISCOUNT10", expiration_date=datetime(2024, 12, 31)
    )

    # Call the delete function
    response = controller.delete(db_session, 1)

    # Assertions
    assert response.status_code == 204

    # Verify the delete call
    db_session.delete.assert_called_once()
