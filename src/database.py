from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, String, BigInteger, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from dotenv import load_dotenv
import os
from pydantic import BaseModel

# Загрузка переменных окружения из файла .env
load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

engin = create_async_engine(DATABASE_URL, echo=True, future=True)
AsyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engin, class_=AsyncSession)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

class UserORM(BaseModel):
    telegram_nickname: str
    telegram_id: int

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    uid = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True)
    telegram_nickname = Column(String, unique=True, index=True)
    registered_at = Column(DateTime(timezone=True), default=func.now())

