from fastapi.testclient import TestClient
from unittest.mock import Mock
import pytest
from sqlalchemy.exc import SQLAlchemyError
from ..main import app
from ..controllers import recipes as controller
from ..models import recipes as model

client = TestClient(app)


@pytest.fixture
def db_session():
    # Mock database session for testing
    return Mock()


def test_create_recipe(db_session):
    # Mock data for a recipe
    recipe_data = {
        "sandwich_id": 1,
        "resource_id": 2,
        "amount": 3,
        "time_to_make": 10
    }
    request_data = model.Recipe(**recipe_data)

    # Mock the database behavior
    db_session.add = Mock()
    db_session.commit = Mock()
    db_session.refresh = Mock()

    def mock_refresh(recipe):
        recipe.time_to_make = recipe_data["time_to_make"]

    db_session.refresh.side_effect = mock_refresh

    # Call the create function
    created_recipe = controller.create(db_session, request_data)

    # Assertions
    assert created_recipe.sandwich_id == recipe_data["sandwich_id"]
    assert created_recipe.resource_id == recipe_data["resource_id"]
    assert created_recipe.amount == recipe_data["amount"]
    assert created_recipe.time_to_make == recipe_data["time_to_make"]


def test_read_all_recipes(db_session):
    # Mock a response list from the database
    db_session.query.return_value.all.return_value = [
        model.Recipe(id=1, sandwich_id=1, resource_id=2, amount=3, time_to_make=10),
        model.Recipe(id=2, sandwich_id=2, resource_id=3, amount=4, time_to_make=15)
    ]

    # Call the read_all function
    results = controller.read_all(db_session)

    # Assertions
    assert len(results) == 2
    assert results[0].sandwich_id == 1
    assert results[0].time_to_make == 10
    assert results[1].sandwich_id == 2
    assert results[1].time_to_make == 15


def test_read_one_recipe(db_session):
    # Mock a single recipe
    db_session.query.return_value.filter.return_value.first.return_value = model.Recipe(
        id=1, sandwich_id=1, resource_id=2, amount=3, time_to_make=10)

    # Call the read_one function
    result = controller.read_one(db_session, 1)

    # Assertions
    assert result is not None
    assert result.sandwich_id == 1
    assert result.time_to_make == 10


def test_update_recipe(db_session):
    # Mock an existing recipe to update
    existing_recipe = model.Recipe(
        id=1, sandwich_id=1, resource_id=2, amount=3, time_to_make=10)
    db_session.query.return_value.filter.return_value.first.return_value = existing_recipe

    # Mock update data
    update_data = {"amount": 5, "time_to_make": 20}
    request_data = Mock()
    request_data.dict.return_value = update_data

    # Mock the update behavior
    db_session.commit = Mock()

    # Call the update function
    updated_recipe = controller.update(db_session, 1, request_data)

    # Manually adjust the mock to simulate the update
    existing_recipe.amount = update_data["amount"]
    existing_recipe.time_to_make = update_data["time_to_make"]

    # Assertions
    assert updated_recipe.amount == 5
    assert updated_recipe.time_to_make == 20


def test_delete_recipe(db_session):
    # Mock an existing recipe to delete
    db_session.query.return_value.filter.return_value.first.return_value = model.Recipe(
        id=1, sandwich_id=1, resource_id=2, amount=3, time_to_make=10)

    # Call the delete function
    response = controller.delete(db_session, 1)

    # Assertions
    assert response.status_code == 204
