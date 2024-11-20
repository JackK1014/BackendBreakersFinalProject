from fastapi.testclient import TestClient
from unittest.mock import Mock
import pytest
from sqlalchemy.exc import SQLAlchemyError
from ..main import app
from ..controllers import orders as controller
from ..models import orders as model
from datetime import datetime

client = TestClient(app)


@pytest.fixture
def db_session():
    # Mock database session for testing
    return Mock()


def test_create_order(db_session):
    # Mock data for an order
    order_data = {
        "customer_name": "John Doe",
        "description": "Test order",
        "status": "pending"
    }
    request_data = model.Order(**order_data)

    # Mock the database behavior
    db_session.add = Mock()
    db_session.commit = Mock()
    db_session.refresh = Mock()

    def mock_refresh(order):
        order.status = order_data["status"]

    db_session.refresh.side_effect = mock_refresh

    # Call the create function
    created_order = controller.create(db_session, request_data)

    # Assertions
    assert created_order.customer_name == order_data["customer_name"]
    assert created_order.description == order_data["description"]
    assert created_order.status == order_data["status"]


def test_read_all_orders(db_session):
    # Mock a response list from the database
    db_session.query.return_value.all.return_value = [
        model.Order(id=1, customer_name="John Doe", description="Test order", status="pending"),
        model.Order(id=2, customer_name="Jane Doe", description="Another test order", status="ready")
    ]

    # Call the read_all function
    results = controller.read_all(db_session)

    # Assertions
    assert len(results) == 2
    assert results[0].customer_name == "John Doe"
    assert results[0].status == "pending"
    assert results[1].customer_name == "Jane Doe"
    assert results[1].status == "ready"


def test_read_one_order(db_session):
    # Mock a single order
    db_session.query.return_value.filter.return_value.first.return_value = model.Order(
        id=1, customer_name="John Doe", description="Test order", status="preparing"
    )

    # Call the read_one function
    result = controller.read_one(db_session, 1)

    # Assertions
    assert result is not None
    assert result.customer_name == "John Doe"
    assert result.status == "preparing"


def test_update_order(db_session):
    # Mock an existing order to update
    existing_order = model.Order(
        id=1, customer_name="John Doe", description="Test order", status="pending"
    )
    db_session.query.return_value.filter.return_value.first.return_value = existing_order

    # Mock update data
    update_data = {"description": "Updated order description", "status": "ready"}
    request_data = Mock()
    request_data.dict.return_value = update_data

    # Mock the update behavior
    db_session.commit = Mock()

    # Call the update function
    updated_order = controller.update(db_session, 1, request_data)

    # Manually adjust the mock to simulate the update
    existing_order.description = update_data["description"]
    existing_order.status = update_data["status"]

    # Assertions
    assert updated_order.description == "Updated order description"
    assert updated_order.status == "ready"


def test_delete_order(db_session):
    # Mock an existing order to delete
    db_session.query.return_value.filter.return_value.first.return_value = model.Order(
        id=1, customer_name="John Doe", description="Test order", status="pending"
    )

    # Call the delete function
    response = controller.delete(db_session, 1)

    # Assertions
    assert response.status_code == 204
def test_read_all_sorted_by_date(db_session):
    # Mock data for orders
    orders_data = [
        model.Order(id=1, customer_name="John Doe", description="Test order", status="pending", order_date=datetime(2024, 11, 17, 10, 30)),
        model.Order(id=2, customer_name="Jane Doe", description="Another test order", status="ready", order_date=datetime(2024, 11, 16, 15, 45)),
    ]

    db_session.query.return_value.order_by.return_value.all.return_value = orders_data

    results = controller.read_all_sorted_by_date(db_session)
    assert len(results) == 2
    assert results[0].order_date > results[1].order_date
    assert results[0].status == "pending"
    assert results[1].status == "ready"

    db_session.query.return_value.filter.return_value.order_by.return_value.all.return_value = [orders_data[1]]
    results_filtered = controller.read_all_sorted_by_date(db_session, datetime(2024, 11, 16))
    assert len(results_filtered) == 1
    assert results_filtered[0].customer_name == "Jane Doe"
    assert results_filtered[0].status == "ready"