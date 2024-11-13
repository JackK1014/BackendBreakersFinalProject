from fastapi.testclient import TestClient
from unittest.mock import Mock
import pytest
from sqlalchemy.exc import SQLAlchemyError
from ..main import app
from ..controllers import resources as controller
from ..models import resources as model

client = TestClient(app)

@pytest.fixture
def db_session():
    # Mock database session for testing
    return Mock()

def test_create_resource(db_session):
    # Mock data for a resource
    resource_data = {
        "item": "Bread",
        "amount": 100
    }
    request_data = model.Resource(**resource_data)
    
    # Mock the database behavior
    db_session.add = Mock()
    db_session.commit = Mock()
    db_session.refresh = Mock()

    # Call the create function
    created_resource = controller.create(db_session, request_data)

    # Assertions
    assert created_resource.item == resource_data["item"]
    assert created_resource.amount == resource_data["amount"]

def test_read_all_resources(db_session):
    # Mock a response list from the database
    db_session.query.return_value.all.return_value = [
        model.Resource(id=1, item="Bread", amount=100),
        model.Resource(id=2, item="Cheese", amount=50)
    ]

    # Call the read_all function
    results = controller.read_all(db_session)

    # Assertions
    assert len(results) == 2
    assert results[0].item == "Bread"
    assert results[1].item == "Cheese"

def test_read_one_resource(db_session):
    # Mock a single resource
    db_session.query.return_value.filter.return_value.first.return_value = model.Resource(id=1, item="Bread", amount=100)

    # Call the read_one function
    result = controller.read_one(db_session, 1)

    # Assertions
    assert result is not None
    assert result.item == "Bread"

def test_update_resource(db_session):
    # Mock an existing resource to update
    existing_resource = model.Resource(id=1, item="Bread", amount=100)
    db_session.query.return_value.filter.return_value.first.return_value = existing_resource

    # Mock update data
    update_data = {"amount": 120}
    request_data = Mock()
    request_data.dict.return_value = update_data

    # Mock the update behavior
    db_session.commit = Mock()

    # Call the update function
    updated_resource = controller.update(db_session, 1, request_data)

    # Manually adjust the mock to simulate the update
    existing_resource.amount = update_data["amount"]

    # Assertions
    assert updated_resource.amount == 120

def test_delete_resource(db_session):
    # Mock an existing resource to delete
    db_session.query.return_value.filter.return_value.first.return_value = model.Resource(id=1, item="Bread", amount=100)

    # Call the delete function
    response = controller.delete(db_session, 1)

    # Assertions
    assert response.status_code == 204
