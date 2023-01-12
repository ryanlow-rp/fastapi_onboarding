from app.api.models import ArtifactSchema
from app.Database import artifacts, database


async def post(payload: ArtifactSchema):
    query = artifacts.insert().values(
        name=payload.name, element=payload.element, level=payload.level
    )
    return await database.execute(query=query)


async def put(id: int, payload: ArtifactSchema):
    query = (
        artifacts.update()
        .where(id == artifacts.c.id)
        .values(level=payload.level, name=payload.name, element=payload.element)
        .returning(artifacts.c.id)
    )
    return await database.execute(query=query)


async def get_by_name(name: str):
    query = artifacts.select().where(name == artifacts.c.name)
    return await database.fetch_one(query=query)


async def get_all():
    query = artifacts.select()
    return await database.fetch_all(query=query)


async def get_artifact_by_level(level: int):
    query = artifacts.select().where(level == artifacts.c.level)
    return await database.fetch_all(query=query)


async def delete(id: int):
    query = artifacts.delete().where(id == artifacts.c.id)
    return await database.execute(query=query)
