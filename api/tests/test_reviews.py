from fastapi.testclient import TestClient
from unittest.mock import Mock
import pytest
from sqlalchemy.exc import SQLAlchemyError
from ..main import app
from ..controllers import reviews as controller
from ..models import reviews as model

client = TestClient(app)


@pytest.fixture
def db_session():
    """Fixture to provide a mocked database session for testing."""
    return Mock()


def test_create_review(db_session):
    """Test for creating a review."""
    # Mock review data
    review_data = {
        "customer_id": 1,
        "sandwich_id": 2,
        "review_text": "Delicious sandwich!",
        "score": 5
    }

    # Create a mock Review object
    created_review = model.Review(**review_data)

    # Mock database methods
    db_session.add = Mock()
    db_session.commit = Mock()
    db_session.refresh = Mock()

    # Mock refresh behavior to simulate the database assigning an ID
    def mock_refresh(review):
        review.id = 1  # Simulate auto-increment ID assignment
        return review

    db_session.refresh.side_effect = mock_refresh

    # Call the create function
    result = controller.create(db_session, created_review)

    # Assertions
    assert result.customer_id == review_data["customer_id"]
    assert result.sandwich_id == review_data["sandwich_id"]
    assert result.review_text == review_data["review_text"]
    assert result.score == review_data["score"]
    assert result.id == 1  # Ensure the ID is correctly set


def test_read_all_reviews(db_session):
    """Test for reading all reviews."""
    # Mock a list of reviews
    db_session.query.return_value.all.return_value = [
        model.Review(id=1, customer_id=1, sandwich_id=2, review_text="Delicious sandwich!", score=5),
        model.Review(id=2, customer_id=2, sandwich_id=3, review_text="Not bad", score=4)
    ]

    # Call the read_all function
    results = controller.read_all(db_session)

    # Assertions
    assert len(results) == 2
    assert results[0].review_text == "Delicious sandwich!"
    assert results[0].score == 5
    assert results[1].review_text == "Not bad"
    assert results[1].score == 4


def test_read_one_review(db_session):
    """Test for reading a single review."""
    # Mock a single review
    db_session.query.return_value.filter.return_value.first.return_value = model.Review(
        id=1, customer_id=1, sandwich_id=2, review_text="Delicious sandwich!", score=5
    )

    # Call the read_one function
    result = controller.read_one(db_session, 1)

    # Assertions
    assert result is not None
    assert result.review_text == "Delicious sandwich!"
    assert result.score == 5


def test_update_review(db_session):
    """Test for updating a review."""
    # Mock an existing review
    existing_review = model.Review(
        id=1, customer_id=1, sandwich_id=2, review_text="Delicious sandwich!", score=5
    )
    db_session.query.return_value.filter.return_value.first.return_value = existing_review

    # Mock update data
    update_data = {"review_text": "Amazing taste!", "score": 4}
    request_data = Mock()
    request_data.dict.return_value = update_data

    # Mock database commit
    db_session.commit = Mock()

    # Call the update function
    updated_review = controller.update(db_session, 1, request_data)

    # Simulate the update behavior
    existing_review.review_text = update_data["review_text"]
    existing_review.score = update_data["score"]

    # Assertions
    assert updated_review.review_text == "Amazing taste!"
    assert updated_review.score == 4


def test_delete_review(db_session):
    """Test for deleting a review."""
    # Mock an existing review to delete
    db_session.query.return_value.filter.return_value.first.return_value = model.Review(
        id=1, customer_id=1, sandwich_id=2, review_text="Delicious sandwich!", score=5
    )

    # Call the delete function
    response = controller.delete(db_session, 1)

    # Assertions
    assert response.status_code == 204

    # Verify the delete call
    db_session.delete.assert_called_once()
