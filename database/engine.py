from sqlalchemy import BigInteger
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, mapped_column

from config import DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pk = mapped_column(BigInteger, primary_key=True)


async def init_db():
    async with engine.begin() as conn:
        # Base.metadata.create_all(conn)
        await conn.run_sync(Base.metadata.create_all)

