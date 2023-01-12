from fastapi import APIRouter, HTTPException
from app.api import crud
from app.api.models import ArtifactDB, ArtifactSchema
from asyncpg.exceptions import UniqueViolationError

from typing import List

router = APIRouter()


@router.post("/add_artifact", status_code=201)
async def add_artifact(payload: ArtifactSchema):
    try:
        artifact_id = await crud.post(payload)
    except UniqueViolationError as e:
        raise HTTPException(status_code=409, detail="name already exists")

    response_object = {
        "id": artifact_id,
        "name": payload.name,
        "element": payload.element,
        "level": payload.level,
    }
    return response_object


@router.put("/increase_artifact_level")
async def increase_artifact_level(name: str, level_increase: int):
    if level_increase < 0:
        raise HTTPException(status_code=422, detail="level cannot be negative")

    artifact = await crud.get_by_name(name)
    if not artifact:
        return dict()

    artifact.level = artifact.level + level_increase
    artifact_id = await crud.put(artifact.id, artifact)

    response_object = {
        "id": artifact_id,
        "name": artifact.name,
        "element": artifact.element,
        "level": artifact.level,
    }
    return response_object


# @router.get("/get_all_artifacts")
# async def get_all_artifacts():
#     artifacts = await crud.get_all()
#     items = list()
#     for artifact in artifacts:
#         print("hello")
#         print(artifact)
#         items.append({artifact.name : artifact})
#     response_object = {"all_artifacts": items}
#     return response_object


@router.get("/get_all_artifacts")
async def get_all_artifacts():
    artifacts = await crud.get_all()
    response_object = {"all_artifacts": artifacts}
    return response_object


@router.get("/get_artifact_by_name")
async def get_artifact_by_name(name: str):
    artifact = await crud.get_by_name(name)
    if not artifact:
        return dict()
    return artifact


@router.get("/get_artifact_by_level")
async def get_artifact_by_level(level: int):
    values = await crud.get_artifact_by_level(level)
    response_object = {"all_artifacts": values}
    return response_object


@router.put("/delete_artifact_by_name")
async def delete_artifact_by_name(name: str):
    artifact = await crud.get_by_name(name)
    if not artifact:
        raise HTTPException(status_code=404, detail="name does not exist")

    await crud.delete(artifact.id)
    response_object = {
        "id": artifact.id,
        "name": artifact.name,
        "element": artifact.element,
        "level": artifact.level,
    }
    return response_object
