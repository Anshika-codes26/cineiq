from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
import structlog

from app.core.config import settings

logger = structlog.get_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("cineiq_starting", host=settings.backend_host, port=settings.backend_port)
    yield
    # Shutdown
    logger.info("cineiq_stopped")

app = FastAPI(
    title="CINEIQ API",
    description="AI-Powered Movie Recommendations and Social Discovery",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    latency = int((time.time() - start) * 1000)
    
    logger.info(
        "http_request",
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
        latency_ms=latency
    )
    
    return response

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error("unhandled_exception", error=str(exc), path=request.url.path)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})

from app.api.v1 import api_router
app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    checks = {}
    
    # Check Redis
    try:
        from app.db.session import get_redis
        redis = get_redis()
        if redis:
            redis.ping()
            checks["redis"] = "ok"
        else:
            checks["redis"] = "not_configured"
    except Exception as e:
        checks["redis"] = f"error: {str(e)[:100]}"
        
    # Check Gemini API
    checks["gemini_api"] = "configured" if settings.gemini_api_key else "not_configured"
    
    # Define required services that must be configured and operational for "healthy"
    required_services = {"redis", "gemini_api"}
    
    # Determine if any required service is not configured
    any_required_not_configured = any(
        service in required_services and v == "not_configured"
        for service, v in checks.items()
    )
    
    # Determine if any required service has an error
    any_required_error = any(
        service in required_services and v.startswith("error:")
        for service, v in checks.items()
    )
    
    if any_required_not_configured:
        overall_status = "not_configured"
    elif any_required_error:
        overall_status = "degraded"
    else:
        # All required services are ok/configured; check optional services
        any_optional_error = any(
            service not in required_services and v.startswith("error:")
            for service, v in checks.items()
        )
        overall_status = "degraded" if any_optional_error else "healthy"
    
    return {
        "status": overall_status,
        "checks": checks
    }
