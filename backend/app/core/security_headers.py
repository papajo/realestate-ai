"""
Security headers middleware for FastAPI application.
Implements OWASP recommended security headers.
"""
from fastapi import Request
from fastapi.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Add security headers to all responses to protect against common web vulnerabilities.
    """
    
    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)
        
        # X-Content-Type-Options: Prevent MIME type sniffing
        response.headers["X-Content-Type-Options"] = "nosniff"
        
        # X-Frame-Options: Prevent clickjacking attacks
        response.headers["X-Frame-Options"] = "DENY"
        
        # X-XSS-Protection: Enable XSS protection in older browsers
        response.headers["X-XSS-Protection"] = "1; mode=block"
        
        # Strict-Transport-Security: Force HTTPS (in production)
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        # Content-Security-Policy: Prevent XSS and data injection attacks
        response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'"
        
        # Referrer-Policy: Control referrer information
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        # Permissions-Policy: Control browser features
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        
        return response
