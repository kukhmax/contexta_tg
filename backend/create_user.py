import asyncio
from app.api.deps import get_db
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from app.core.config import settings
from sqlalchemy.ext.asyncio import create_async_engine

async def create_dev_user():
    # Setup database connection
    print(f"Connecting to {settings.DATABASE_URL}")
    db_url = str(settings.DATABASE_URL).replace("postgresql://", "postgresql+asyncpg://")
    engine = create_async_engine(db_url)
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        # Check if user exists
        stmt = select(User).where(User.telegram_id == 123456789)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            print("Creating dev user (ID: 123456789)...")
            new_user = User(
                telegram_id=123456789,
                username="guest_dev",
                first_name="Guest",
                language_code="en"
            )
            session.add(new_user)
            await session.commit()
            print("User created successfully!")
        else:
            print("Dev user already exists.")

    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(create_dev_user())
