import asyncio
import os
import sys
from datetime import date
from dotenv import load_dotenv

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, String, Date, select, update, delete

# Windows event loop
if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Load env variables
load_dotenv()
USER = os.getenv("POSTGRES_USER_ID")
PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB = os.getenv("POSTGRES_DATABASE")
HOST = os.getenv("POSTGRES_HOST")
PORT = os.getenv("POSTGRES_PORT")

# Async DB URL
DATABASE_URL = f"postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"

# SQLAlchemy setup
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

# Define ORM model
class UserCredentials(Base):
    __tablename__ = 'user_credentials'

    firstname = Column(String(25))
    lastname = Column(String(25))
    dob = Column(Date)
    email = Column(String(50), primary_key=True)
    phone_number = Column(String(15), unique=True)

# Create table
async def create_user_credentials_table():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Table created.")

# Insert
async def insert_user_credentials(firstname, lastname, dob, email, phone_number):
    async with SessionLocal() as session:
        async with session.begin():
            user = UserCredentials(
                firstname=firstname,
                lastname=lastname,
                dob=dob,
                email=email,
                phone_number=phone_number
            )
            session.add(user)
        return True

# Read
async def get_user_credentials(email):
    async with SessionLocal() as session:
        result = await session.execute(
            select(UserCredentials).where(UserCredentials.email == email)
        )
        return result.scalar_one_or_none()

# Update
async def update_user_credentials(email, firstname, lastname, dob, phone_number):
    async with SessionLocal() as session:
        async with session.begin():
            await session.execute(
                update(UserCredentials)
                .where(UserCredentials.email == email)
                .values(
                    firstname=firstname,
                    lastname=lastname,
                    dob=dob,
                    phone_number=phone_number
                )
            )
        return True

# Delete
async def delete_user_credentials(email):
    async with SessionLocal() as session:
        async with session.begin():
            await session.execute(
                delete(UserCredentials).where(UserCredentials.email == email)
            )
        return True

# Main test
async def main():

    # await create_user_credentials_table()
    user = await get_user_credentials("varun@gmail.com")
    if user:
        print("User found:", user.firstname, user.lastname, user.dob, user.email, user.phone_number)
    else:
        print("No user found with that email")
    # You can test other functions here too

if __name__ == "__main__":
    asyncio.run(main())
    



    # await insert_user_credentials(
    # firstname="Varun",
    # lastname="Reddi",
    # dob=date(2000, 1, 1),
    # email="varun@gmail.com",
    # phone_number="9876543210"
    # )
    # user = await get_user_credentials("varun@gmail.com")
    # print(user)
