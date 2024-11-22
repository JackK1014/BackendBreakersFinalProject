from fastapi.testclient import TestClient
from unittest.mock import Mock
import pytest
from sqlalchemy.exc import SQLAlchemyError
from ..main import app
from ..controllers import customers as controller
from ..models import customers as model

client = TestClient(app)


@pytest.fixture
def db_session():
    """Fixture to provide a mocked database session for testing."""
    return Mock()


def test_create_customer(db_session):
    """Test for creating a customer."""
    # Mock customer data
    customer_data = {
        "name": "John Doe",
        "email": "johndoe@example.com",
        "phone_number": "1234567890",
        "address": "123 Elm Street"
    }

    # Create a mock Customer object
    created_customer = model.Customer(**customer_data)

    # Mock database methods
    db_session.add = Mock()
    db_session.commit = Mock()
    db_session.refresh = Mock()

    # Mock refresh behavior to simulate the database assigning an ID
    def mock_refresh(customer):
        customer.id = 1  # Simulate auto-increment ID assignment
        return customer

    db_session.refresh.side_effect = mock_refresh

    # Call the create function
    result = controller.create(db_session, created_customer)

    # Assertions
    assert result.name == customer_data["name"]
    assert result.email == customer_data["email"]
    assert result.phone_number == customer_data["phone_number"]
    assert result.address == customer_data["address"]
    assert result.id == 1  # Ensure the ID is correctly set


def test_read_all_customers(db_session):
    """Test for reading all customers."""
    # Mock a list of customers
    db_session.query.return_value.all.return_value = [
        model.Customer(id=1, name="John Doe", email="johndoe@example.com", phone_number="1234567890", address="123 Elm Street"),
        model.Customer(id=2, name="Jane Smith", email="janesmith@example.com", phone_number="0987654321", address="456 Maple Avenue")
    ]

    # Call the read_all function
    results = controller.read_all(db_session)

    # Assertions
    assert len(results) == 2
    assert results[0].name == "John Doe"
    assert results[0].email == "johndoe@example.com"
    assert results[1].name == "Jane Smith"
    assert results[1].email == "janesmith@example.com"


def test_read_one_customer(db_session):
    """Test for reading a single customer."""
    # Mock a single customer
    db_session.query.return_value.filter.return_value.first.return_value = model.Customer(
        id=1, name="John Doe", email="johndoe@example.com", phone_number="1234567890", address="123 Elm Street"
    )

    # Call the read_one function
    result = controller.read_one(db_session, 1)

    # Assertions
    assert result is not None
    assert result.name == "John Doe"
    assert result.email == "johndoe@example.com"


def test_update_customer(db_session):
    """Test for updating a customer."""
    # Mock an existing customer
    existing_customer = model.Customer(
        id=1, name="John Doe", email="johndoe@example.com", phone_number="1234567890", address="123 Elm Street"
    )
    db_session.query.return_value.filter.return_value.first.return_value = existing_customer

    # Mock update data
    update_data = {"name": "Johnathan Doe", "email": "johnathan.doe@example.com"}
    request_data = Mock()
    request_data.dict.return_value = update_data

    # Mock database commit
    db_session.commit = Mock()

    # Call the update function
    updated_customer = controller.update(db_session, 1, request_data)

    # Simulate the update behavior
    existing_customer.name = update_data["name"]
    existing_customer.email = update_data["email"]

    # Assertions
    assert updated_customer.name == "Johnathan Doe"
    assert updated_customer.email == "johnathan.doe@example.com"


def test_delete_customer(db_session):
    """Test for deleting a customer."""
    # Mock an existing customer to delete
    db_session.query.return_value.filter.return_value.first.return_value = model.Customer(
        id=1, name="John Doe", email="johndoe@example.com", phone_number="1234567890", address="123 Elm Street"
    )

    # Call the delete function
    response = controller.delete(db_session, 1)

    # Assertions
    assert response.status_code == 204

    # Verify the delete call
    db_session.delete.assert_called_once()
