#!/usr/bin/env python3
"""Create database tables"""
import asyncio
from app.core.database import engine, Base
from app.models import User, Lead, Conversation, PropertyAnalysis, CashBuyer

async def create_tables():
    print("Creating database tables...")
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("✓ Tables created successfully!")
        return True
    except Exception as e:
        print(f"✗ Error creating tables: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(create_tables())
    exit(0 if success else 1)

