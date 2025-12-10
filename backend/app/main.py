from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api.routes import auth
from app.config import settings
from app.database import db


app = FastAPI(
    title="Authentication API",
    description="Production-grade authentication system",
    version="1.0.0"
)

#CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

#security headers middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    if settings.ENVOIRONMENT == "production":
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response

#includes router
app.include_router(auth.router)

#root endpoint
@app.get("/")
async def root():
    return {
        "message": "Authentication API",
        "version": "1.0.0",
        "status": "running"
    }

#health check
@app.get("/health")
async def health():
    return {"status": "healthy"}

#startup event
@app.on_event("startup")
async def startup_event():
    """
    initialize database connection on startup
    """
    db.connect()
    print("server started successfully")

#shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """
    close database connection on shutdown
    """
    db.disconnect()
    print("server shut down")

#global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "path": str(request.url)
        }
    )