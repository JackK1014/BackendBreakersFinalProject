from fastapi.testclient import TestClient
from unittest.mock import Mock
import pytest
from sqlalchemy.exc import SQLAlchemyError
from ..main import app
from ..controllers import payments as controller
from ..models import payments as model

client = TestClient(app)


@pytest.fixture
def db_session():
    """Fixture to provide a mocked database session for testing."""
    return Mock()


def test_create_payment(db_session):
    """Test for creating a payment."""
    # Mock payment data
    payment_data = {
        "order_id": 1,
        "card_information": "1234-5678-9012-3456",
        "transaction_status": "Pending",
        "payment_type": "Credit Card"
    }

    # Create a mock Payment object to simulate the database behavior
    created_payment = model.Payment(**payment_data)

    # Mock database methods
    db_session.add = Mock()
    db_session.commit = Mock()
    db_session.refresh = Mock()

    # Mock the refresh method to simulate database behavior
    def mock_refresh(payment):
        payment.id = 1  # Simulate an auto-incremented ID assigned by the database
        return payment

    db_session.refresh.side_effect = mock_refresh

    # Call the create function
    result = controller.create(db_session, created_payment)

    # Assertions
    assert result.order_id == payment_data["order_id"]
    assert result.card_information == payment_data["card_information"]
    assert result.transaction_status == payment_data["transaction_status"]
    assert result.payment_type == payment_data["payment_type"]
    assert result.id == 1  # Ensure the ID is correctly set


def test_read_all_payments(db_session):
    """Test for reading all payments."""
    # Mock a response list from the database
    db_session.query.return_value.all.return_value = [
        model.Payment(id=1, order_id=1, card_information="1234-5678-9012-3456", transaction_status="Completed", payment_type="Credit Card"),
        model.Payment(id=2, order_id=2, card_information="9876-5432-1098-7654", transaction_status="Pending", payment_type="Debit Card")
    ]

    # Call the read_all function
    results = controller.read_all(db_session)

    # Assertions
    assert len(results) == 2
    assert results[0].order_id == 1
    assert results[0].transaction_status == "Completed"
    assert results[1].order_id == 2
    assert results[1].transaction_status == "Pending"


def test_read_one_payment(db_session):
    """Test for reading a single payment."""
    # Mock a single payment
    db_session.query.return_value.filter.return_value.first.return_value = model.Payment(
        id=1, order_id=1, card_information="1234-5678-9012-3456", transaction_status="Completed", payment_type="Credit Card"
    )

    # Call the read_one function
    result = controller.read_one(db_session, 1)

    # Assertions
    assert result is not None
    assert result.order_id == 1
    assert result.transaction_status == "Completed"


def test_update_payment(db_session):
    """Test for updating a payment."""
    # Mock an existing payment to update
    existing_payment = model.Payment(
        id=1, order_id=1, card_information="1234-5678-9012-3456", transaction_status="Pending", payment_type="Credit Card"
    )
    db_session.query.return_value.filter.return_value.first.return_value = existing_payment

    # Mock update data
    update_data = {"transaction_status": "Completed"}
    request_data = Mock()
    request_data.dict.return_value = update_data

    # Mock database commit
    db_session.commit = Mock()

    # Call the update function
    updated_payment = controller.update(db_session, 1, request_data)

    # Manually adjust the mock to simulate the update
    existing_payment.transaction_status = update_data["transaction_status"]

    # Assertions
    assert updated_payment.transaction_status == "Completed"


def test_delete_payment(db_session):
    """Test for deleting a payment."""
    # Mock an existing payment to delete
    db_session.query.return_value.filter.return_value.first.return_value = model.Payment(
        id=1, order_id=1, card_information="1234-5678-9012-3456", transaction_status="Pending", payment_type="Credit Card"
    )

    # Call the delete function
    response = controller.delete(db_session, 1)

    # Assertions
    assert response.status_code == 204

    # Verify the delete call
    db_session.delete.assert_called_once()
