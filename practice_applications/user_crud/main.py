from uuid import uuid4
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import Column, String, DateTime, create_engine, func

DATABASE_URL = "postgresql://postgres:postgresdb@localhost/simple_user"
engine = create_engine(DATABASE_URL)
local_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    global local_session
    db = local_session()
    try:
        yield db
    finally:
        db.close()


class User(Base):
    __tablename__ = "user"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True
    )
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=func.now())


class UserCreate(BaseModel):
    name: str
    email: EmailStr


app = FastAPI()

Base.metadata.create_all(bind=engine)
