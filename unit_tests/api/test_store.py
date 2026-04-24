import pytest
from flask.testing import FlaskClient
from werkzeug.test import TestResponse

from database.models import StoreFactory, StoreModel


@pytest.fixture()
def store():
    return StoreFactory.create()


def test_get_stores(test_app_client):
    response = test_app_client.get("/store")

    assert response.status_code == 200


def test_get_specific_store(test_app_client: FlaskClient):
    response: TestResponse = test_app_client.get("/store/3")
    assert response.status_code == 404


def test_create_store_returns_error_with_invalid_fields(test_app_client: FlaskClient):
    store_data = {"id": 1, "name": "store test"}
    response: TestResponse = test_app_client.post("/store", json=store_data)

    assert response.status_code == 422

    response_json = response.get_json()
    assert response_json.get("errors") == {"json": {"id": ["Unknown field."]}}


def test_create_store_returns_success(test_app_client: FlaskClient, test_db_session):
    store_data = {"name": "test store name"}
    response: TestResponse = test_app_client.post("/store", json=store_data)

    assert response.status_code == 201

    existing_store = (
        test_db_session.query(StoreModel).filter(StoreModel.id == 1).one_or_none()
    )

    assert existing_store.name == "test store name"
