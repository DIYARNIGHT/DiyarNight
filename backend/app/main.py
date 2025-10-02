from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import router
from app.database.connection import load_csv_data
import uvicorn

app = FastAPI(
    title="Superonline SmartNet API",
    description="Fiber Kapsama, Kota Takibi ve Dinamik Paket Önerisi API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    """Initialize database with CSV data on startup"""
    await load_csv_data()

@app.get("/")
async def read_root():
    """API ana sayfa"""
    return {
        "message": "Superonline SmartNet API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "users": "/api/v1/users",
            "addresses": "/api/v1/addresses", 
            "plans": "/api/v1/plans",
            "addons": "/api/v1/addons",
            "support": "/api/v1/support",
            "usage": "/api/v1/usage"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Superonline SmartNet API is running"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )