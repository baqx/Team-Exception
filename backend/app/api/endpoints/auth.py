from fastapi import APIRouter, HTTPException, Depends, Header, Body
from typing import Optional, Dict, Any
from pydantic import BaseModel, EmailStr
from app.services import user_service

router = APIRouter()

class RegisterRequest(BaseModel):
    email: str
    password: str
    name: str

class LoginRequest(BaseModel):
    email: str
    password: str

class RechargeRequest(BaseModel):
    amount: int = 25

async def get_current_user(authorization: Optional[str] = Header(None)) -> Dict[str, Any]:
    token = None
    if authorization:
        parts = authorization.split(" ")
        if len(parts) == 2 and parts[0].lower() == "bearer":
            token = parts[1]
        else:
            token = authorization

    if not token:
        raise HTTPException(status_code=401, detail="Authentication token required.")
        
    user = user_service.get_user_by_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired session. Please log in again.")
    return user

@router.post("/auth/register")
async def register(req: RegisterRequest):
    if not req.email or "@" not in req.email:
        raise HTTPException(status_code=400, detail="A valid email address is required.")
    if not req.password or len(req.password) < 4:
        raise HTTPException(status_code=400, detail="Password must be at least 4 characters.")
    if not req.name or len(req.name.strip()) == 0:
        req.name = req.email.split("@")[0].title()

    try:
        user_data = user_service.create_user(req.email, req.password, req.name)
        return {
            "success": True,
            "message": "Account created successfully with 50 chalkboard credits!",
            "token": user_data["token"],
            "user": {
                "id": user_data["id"],
                "email": user_data["email"],
                "name": user_data["name"],
                "credits": user_data["credits"]
            }
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

@router.post("/auth/login")
async def login(req: LoginRequest):
    if not req.email or not req.password:
        raise HTTPException(status_code=400, detail="Email and password are required.")
        
    user_data = user_service.authenticate_user(req.email, req.password)
    if not user_data:
        raise HTTPException(status_code=401, detail="Incorrect email or password.")
        
    return {
        "success": True,
        "token": user_data["token"],
        "user": {
            "id": user_data["id"],
            "email": user_data["email"],
            "name": user_data["name"],
            "credits": user_data["credits"]
        }
    }

@router.get("/auth/me")
async def get_me(user: Dict[str, Any] = Depends(get_current_user)):
    return {
        "user": user
    }

@router.post("/user/credits/recharge")
async def recharge_credits(
    req: RechargeRequest = Body(default=RechargeRequest()),
    user: Dict[str, Any] = Depends(get_current_user)
):
    add_amount = max(5, min(req.amount, 100))
    new_balance = user_service.add_credits(user["id"], add_amount)
    return {
        "success": True,
        "added": add_amount,
        "credits": new_balance,
        "message": f"Added {add_amount} classroom credits to your account!"
    }

@router.get("/user/history")
async def get_user_history(user: Dict[str, Any] = Depends(get_current_user)):
    jobs = user_service.get_user_jobs(user["id"])
    return {
        "jobs": jobs,
        "credits": user["credits"]
    }
