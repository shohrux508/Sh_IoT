# from typing import Any, AsyncGenerator
#
# from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
# from sqlalchemy.pool import StaticPool
# from app.database import Base
# import asyncio
#
# DATABASE_URL = 'sqlite+aiosqlite:///./test.db'
#
# engine_test = create_async_engine(DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)
# SessionTest = async_sessionmaker(engine_test, expire_on_commit=False)
#
#
# async def init_test_db():
#     async with engine_test.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#
#
# async def override_get_session() -> AsyncGenerator[AsyncSession, Any]:
#     print('✅ Using the sqlite session')
#     async with SessionTest() as session:
#         yield session
