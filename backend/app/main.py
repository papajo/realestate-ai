from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.openapi.utils import get_openapi
from contextlib import asynccontextmanager
import uvicorn

from app.core.config import settings
from app.core.database import engine, Base
from app.core.security_headers import SecurityHeadersMiddleware
from app.api.v1.router import api_router
from app.websocket.routes import websocket_endpoint


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("✓ Database tables created/verified")
    except Exception as e:
        print(f"⚠ Warning: Could not connect to database: {e}")
        print("⚠ The app will start but database features will not work.")
        print("⚠ To fix: Set up PostgreSQL and configure DATABASE_URL in .env")
    yield
    # Shutdown
    pass


app = FastAPI(
    title="AI Real Estate Investing API",
    description="Full-stack SaaS application for real estate investing automation",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Security headers middleware
app.add_middleware(SecurityHeadersMiddleware)

# CORS middleware - allow all origins in DEBUG mode for Vercel preview deployments
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.DEBUG else settings.CORS_ORIGINS,  # Allow all in dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Trusted host middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"] if settings.DEBUG else settings.ALLOWED_HOSTS
)

# Include routers
app.include_router(api_router, prefix="/api/v1")

# WebSocket endpoint
app.websocket("/ws")(websocket_endpoint)


@app.get("/")
async def root():
    return {"message": "AI Real Estate Investing API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring.
    
    Returns:
        dict: Status of the application
    """
    return {"status": "healthy", "version": "1.0.0"}


def custom_openapi():
    """
    Custom OpenAPI schema with enhanced documentation.
    """
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="AI Real Estate Investing API",
        version="1.0.0",
        description="Complete API documentation for the Real Estate AI platform",
        routes=app.routes,
    )
    
    # Add authentication info
    openapi_schema["components"]["securitySchemes"] = {
        "Bearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

