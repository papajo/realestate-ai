#!/usr/bin/env python3
"""Test database connection"""
import asyncio
import sys
from app.core.database import engine, AsyncSessionLocal
from app.core.config import settings

async def test_connection():
    print(f"Testing connection to: {settings.DATABASE_URL.replace(settings.DATABASE_URL.split('@')[0].split('//')[1] if '@' in settings.DATABASE_URL else '', '***')}")
    
    try:
        from sqlalchemy import text
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT 1"))
            print("✓ Database connection successful!")
            return True
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        print(f"\nTroubleshooting:")
        print(f"1. Check if PostgreSQL is running: pg_isready")
        print(f"2. Check DATABASE_URL in .env file")
        print(f"3. Verify database exists: psql -U postgres -l | grep realestate_ai")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_connection())
    sys.exit(0 if success else 1)

