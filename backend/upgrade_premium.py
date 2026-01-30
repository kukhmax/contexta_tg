import asyncio
from app.models.user import User, SubscriptionTier
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import select, update
from app.core.config import settings

async def upgrade_user():
    print(f"Connecting to database...")
    # Ensure correct driver
    db_url = str(settings.DATABASE_URL).replace("postgresql://", "postgresql+asyncpg://")
    engine = create_async_engine(db_url)
    
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        telegram_id = 123456789
        print(f"Checking user {telegram_id}...")
        
        stmt = select(User).where(User.telegram_id == telegram_id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if user:
            print(f"User found. Current tier: {user.tier}")
            # Update to Premium
            stmt = update(User).where(User.telegram_id == telegram_id).values(tier=SubscriptionTier.PREMIUM)
            await session.execute(stmt)
            await session.commit()
            print("Successfully upgraded user to PREMIUM! Limits removed.")
        else:
            print("User not found!")

    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(upgrade_user())
