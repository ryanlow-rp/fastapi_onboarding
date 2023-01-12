import json

import pytest

from app.api import crud
from app.api.models import ArtifactDB


def test_create_artifact(test_app, monkeypatch):
    test_request_payload = {"name": "Cat", "element": "Cute", "level": 37}
    test_response_payload = {"id": 1, "name": "Cat", "element": "Cute", "level": 37}

    async def mock_post(payload):
        return 1

    monkeypatch.setattr(crud, "post", mock_post)

    response = test_app.post(
        "/add_artifact",
        content=json.dumps(test_request_payload),
    )

    assert response.status_code == 201
    assert response.json() == test_response_payload


def test_create_artifact_invalid_json(test_app):
    response = test_app.post("/add_artifact", content=json.dumps({"name": "Cat"}))
    assert response.status_code == 422


def test_read_artifact(test_app, monkeypatch):
    test_data = {"id": 1, "name": "Cat", "element": "Cute", "level": 37}
    test_request_payload = {"name": "Cat"}

    async def mock_get(name):
        return test_data

    monkeypatch.setattr(crud, "get_by_name", mock_get)

    response = test_app.get("/get_artifact_by_name?name=Cat")
    assert response.status_code == 200
    assert response.json() == test_data


def test_read_artifact_unknown_name(test_app, monkeypatch):
    async def mock_get(name):
        return None

    monkeypatch.setattr(crud, "get_by_name", mock_get)

    response = test_app.get("/get_artifact_by_name?name=Doggy")
    assert response.status_code == 200
    assert response.json() == {}


def test_read_all_artifacts(test_app, monkeypatch):
    test_data = [
        {"id": 1, "name": "Cat", "element": "Cute", "level": 37},
        {"id": 2, "name": "Doggy", "element": "Adorable", "level": 42},
    ]

    test_response = {
        "all_artifacts": [
            {"id": 1, "name": "Cat", "element": "Cute", "level": 37},
            {"id": 2, "name": "Doggy", "element": "Adorable", "level": 42},
        ]
    }

    async def mock_get_all():
        return test_data

    monkeypatch.setattr(crud, "get_all", mock_get_all)

    response = test_app.get("/get_all_artifacts")
    assert response.status_code == 200
    assert response.json() == test_response


def test_read_all_artifacts_no_data(test_app, monkeypatch):
    test_data = []

    test_response = {"all_artifacts": []}

    async def mock_get_all():
        return test_data

    monkeypatch.setattr(crud, "get_all", mock_get_all)

    response = test_app.get("/get_all_artifacts")
    assert response.status_code == 200
    assert response.json() == test_response


def test_increase_artifact_level_negative_value(test_app, monkeypatch):
    test_update_data = {"name": "Cat", "level_increase": -5}

    async def mock_get(name):
        return True

    monkeypatch.setattr(crud, "get_by_name", mock_get)

    async def mock_put(id, payload):
        return 1

    monkeypatch.setattr(crud, "put", mock_put)

    response = test_app.put(
        "/increase_artifact_level",
        content=json.dumps(test_update_data),
    )
    assert response.status_code == 422


def test_increase_artifact_level(test_app, monkeypatch):
    test_response_payload = {"id": 1, "name": "Cat", "element": "Cute", "level": 42}

    async def mock_get(name):
        return ArtifactDB(
            name="Cat",
            element="Cute",
            level=37,
            id=1,
        )

    monkeypatch.setattr(crud, "get_by_name", mock_get)

    async def mock_put(id, payload):
        return 1

    monkeypatch.setattr(crud, "put", mock_put)

    response = test_app.put("/increase_artifact_level?name=Cat&level_increase=5")

    assert response.status_code == 200
    assert response.json() == test_response_payload


def test_remove_artifact(test_app, monkeypatch):
    test_data = {"id": 1, "name": "Cat", "element": "Cute", "level": 37}

    async def mock_get(name):
        return ArtifactDB(
            name="Cat",
            element="Cute",
            level=37,
            id=1,
        )

    monkeypatch.setattr(crud, "get_by_name", mock_get)

    async def mock_delete(id):
        return id

    monkeypatch.setattr(crud, "delete", mock_delete)

    response = test_app.put("/delete_artifact_by_name?name=Cat")
    assert response.status_code == 200
    assert response.json() == test_data


def test_remove_artifact_incorrect_name(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get_by_name", mock_get)

    response = test_app.put("/delete_artifact_by_name?name=Cat")
    assert response.status_code == 404
    assert response.json()["detail"] == "name does not exist"
