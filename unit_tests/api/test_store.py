import os

import pytest
from flask.testing import FlaskClient
from werkzeug.test import TestResponse

from database.models import StoreFactory, StoreModel
import logging

@pytest.fixture()
def store():
    return StoreFactory.create()


def test_get_stores(test_app_client, caplog):
    caplog.set_level(logging.INFO)
    os.environ["WEATHER_BASE_URL"] = ""
    response = test_app_client.get("/store")

    assert response.status_code == 200

    for m in caplog.messages:
        print(m)


def test_get_specific_store_returns_ok(test_app_client: FlaskClient, store):

    response: TestResponse = test_app_client.get("/store/" + str(store.id))
    assert response.status_code == 200
    response_json = response.get_json()
    assert response_json["id"] == str(store.id)


def test_get_invalid_store_returns_not_found(test_app_client: FlaskClient):
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
