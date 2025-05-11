# import pytest
# from app.database import init_engine, engine, SessionLocal, Base, get_db
#
# # 🔧 Только один вызов — и он инициализирует engine + SessionLocal
# init_engine("sqlite+aiosqlite:///./test.db", use_sqlite=True)
#
# # 🔄 Используем именно SessionLocal, который инициализировался в init_engine
# async def override_get_session():
#     print("✅ Using SQLite test session")
#     async with SessionLocal() as session:
#         yield session
#
# from app.main import create_app
# app = create_app()
# app.dependency_overrides[get_db] = override_get_session
#
# # 🧪 Создаём таблицы один раз
# @pytest.fixture(scope="session", autouse=True)
# async def prepare():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
