import uvicorn
from app.config import settings

if __name__ == "__main__":
    print(f"""
    ╔════════════════════════════════════════╗
    ║   Authentication API Server            ║
    ║   Environment: {settings.ENVOIRONMENT.ljust(24)} ║
    ║   Host: {settings.API_HOST.ljust(31)} ║
    ║   Port: {str(settings.API_PORT).ljust(31)} ║
    ╚════════════════════════════════════════╝
    """)
    
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True if settings.ENVI == "development" else False,
        log_level="info"
    )