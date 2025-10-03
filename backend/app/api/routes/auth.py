from fastapi import APIRouter, HTTPException
from app.models.schemas import LoginRequest, LoginResponse

router = APIRouter(prefix="/auth", tags=["authentication"])

def verify_token(token: str = None):
    """Basit token verification - demo amaçlı"""
    return "demo_user"

@router.post("/login")
async def login(request: LoginRequest):
    if request.username == "mahmutsibal" and request.password == "123457":
        return {
            "success": True,
            "message": "Giriş başarılı",
            "token": "mahmut_token_123",
            "user": {
                "user_id": "U6",
                "username": "mahmutsibal",
                "name": "Mahmut Sibal",
                "email": "mahmut@smartnet.com",
                "role": "user"
            }
        }
    raise HTTPException(status_code=401, detail="Hatalı giriş")

@router.post("/logout")
async def logout():
    return {"success": True, "message": "Çıkış başarılı"}
