async def init_sa_db(engine, Base, *args, **kwargs):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    print("DATABASE SUCCESSFULY INITIALIZED")
