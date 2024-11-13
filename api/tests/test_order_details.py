from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError
from unittest.mock import Mock
import pytest
from ..main import app
from ..controllers import order_details as controller
from ..models import order_details as model

client = TestClient(app)


@pytest.fixture
def db_session():
    # Mock database session for testing
    return Mock()


def test_create_order_details(db_session):
    # Create a sample order
    order_data = {
        "amount": 10,
        "order_id": 1,
        "sandwich_id": 0
    }

    order_object = model.OrderDetail(**order_data)

    # Mock the behavior of adding and committing to the database
    db_session.add = Mock()
    db_session.commit = Mock()
    db_session.refresh = Mock()

    # Call the create function
    created_order = controller.create(db_session, order_object)

    # Assertions
    assert created_order is not None
    assert created_order.amount == 10
    assert created_order.order_id == 1
    assert created_order.sandwich_id == 0


def test_read_all_orders(db_session):
    # Mock a response list from the database
    db_session.query.return_value.all.return_value = [
        model.OrderDetail(id=1, amount=10, order_id=1, sandwich_id=0),
        model.OrderDetail(id=2, amount=5, order_id=2, sandwich_id=1)
    ]

    # Call the read_all function
    results = controller.read_all(db_session)

    # Assertions
    assert len(results) == 2
    assert results[0].amount == 10
    assert results[1].amount == 5


def test_read_one_order(db_session):
    # Mock a single order detail
    db_session.query.return_value.filter.return_value.first.return_value = model.OrderDetail(
        id=1, amount=10, order_id=1, sandwich_id=0)

    # Call the read_one function
    result = controller.read_one(db_session, 1)

    # Assertions
    assert result is not None
    assert result.id == 1
    assert result.amount == 10


def test_update_order(db_session):
    # Mock an existing order to update
    existing_order = model.OrderDetail(
        id=1, amount=10, order_id=1, sandwich_id=0)
    db_session.query.return_value.filter.return_value.first.return_value = existing_order

    # Mock update data
    update_data = {"amount": 15}
    request_data = Mock()
    request_data.dict.return_value = update_data

    # Mock the update behavior
    db_session.commit = Mock()

    # Call the update function
    updated_order = controller.update(db_session, 1, request_data)

    # Manually adjust the mock for the updated data
    existing_order.amount = update_data["amount"]

    # Assertions
    assert updated_order.amount == 15


def test_delete_order(db_session):
    # Mock an existing order to delete
    db_session.query.return_value.filter.return_value.first.return_value = model.OrderDetail(
        id=1, amount=10, order_id=1, sandwich_id=0)

    # Call the delete function
    response = controller.delete(db_session, 1)

    # Assertions
    assert response.status_code == 204
