import asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from fastapi import FastAPI
import pytest
import os
import base64
from sqlmodel import SQLModel
from sqlalchemy.orm import sessionmaker, DeclarativeBase


import models
from dotenv import load_dotenv
load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv('TEST_DATABASE_URL')
async_engine = create_async_engine(
    url=SQLALCHEMY_DATABASE_URL,
    echo=True,
)

# drop all database every time when test complete
@pytest.fixture(scope='session')
async def async_db_engine():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield async_engine

    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

# truncate all table to isolate tests
@pytest.fixture(scope='function')
async def async_db(async_db_engine):
    async_session = sessionmaker(
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
        bind=async_db_engine,
        class_=AsyncSession,
    )

    async with async_session() as session:
        await session.begin()

        yield session

        await session.rollback()

        for table in reversed(SQLModel.metadata.sorted_tables):
            await session.execute(f'TRUNCATE {table.name} CASCADE;')
            await session.commit()
        # await session.close()

@pytest.fixture(scope='session')
def async_client() -> AsyncClient:
    client = AsyncClient(app=FastAPI(), base_url='http://localhost:8000/')
    return client                               

# let test session to know it is running inside event loop
@pytest.fixture(scope='session')
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="module")
def test_user():
    username ="test_user"
    password = "your_password_here"
    return f"Basic {base64.b64encode(f'{username}:{password}'.encode()).decode()}"

@pytest.fixture
async def user(async_db: AsyncSession) -> models.User:
    user = models.User(username='test_user', password='your_password_here')
    async_db.add(user)
    await async_db.commit()
    await async_db.refresh(user)
    return user

@pytest.fixture
async def book(async_db: AsyncSession) -> models.Book:
    book_dict= {
        "title":"sample",
        "author":"sample",
        "genre":"sample",
        "year_published":2014,
        "summary": "Sample Summary"
    }
    book = models.Book(**book_dict)
    async_db.add(book)
    await async_db.commit()
    await async_db.refresh(book)
    import time
    time.sleep(5)
    return book