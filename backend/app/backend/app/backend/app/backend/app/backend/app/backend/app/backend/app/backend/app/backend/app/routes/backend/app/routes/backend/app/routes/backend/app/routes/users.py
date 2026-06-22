from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..database import supabase
from ..schemas import User, UserCreate
from ..auth import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=List[User])
async def get_users(current_user = Depends(get_current_user)):
    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(status_code=403, detail="Not allowed")
    response = supabase.table("users").select("*").execute()
    return response.data

@router.post("/", response_model=User)
async def create_user(user: UserCreate, current_user = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can create users")
    raise HTTPException(status_code=501, detail="Not implemented")
