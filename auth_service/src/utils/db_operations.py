from sqlalchemy.ext.asyncio import AsyncSession


async def add_and_commit(db: AsyncSession, instance):
    db.add(instance)
    await db.commit()


async def refresh_instance(db: AsyncSession, instance):
    await db.refresh(instance)


async def execute_query(db: AsyncSession, query):
    return await db.execute(query)


async def delete_and_commit(db: AsyncSession, instance):
    await db.delete(instance)
    await db.commit()
