"""
Rate limiting middleware for FastAPI application.
Implements token bucket algorithm for request throttling.
"""
from fastapi import HTTPException, status
from datetime import datetime, timedelta
from typing import Dict
import asyncio
from collections import defaultdict

class RateLimiter:
    def __init__(self, calls: int = 100, period: int = 60):
        """
        Initialize rate limiter with token bucket algorithm
        
        Args:
            calls: Number of allowed requests
            period: Time period in seconds
        """
        self.calls = calls
        self.period = period
        self.clients: Dict[str, list] = defaultdict(list)
        
    async def check_rate_limit(self, client_id: str) -> bool:
        """
        Check if client has exceeded rate limit
        
        Args:
            client_id: Unique client identifier (IP, user ID, etc.)
            
        Returns:
            True if request is allowed, False if limit exceeded
        """
        now = datetime.utcnow()
        
        # Remove old timestamps outside the period
        if client_id in self.clients:
            self.clients[client_id] = [
                ts for ts in self.clients[client_id]
                if now - ts < timedelta(seconds=self.period)
            ]
        
        # Check if limit exceeded
        if len(self.clients[client_id]) >= self.calls:
            return False
            
        # Add current timestamp
        self.clients[client_id].append(now)
        return True

# Global rate limiter instances
api_limiter = RateLimiter(calls=100, period=60)  # 100 requests per minute
auth_limiter = RateLimiter(calls=10, period=60)  # 10 auth attempts per minute
