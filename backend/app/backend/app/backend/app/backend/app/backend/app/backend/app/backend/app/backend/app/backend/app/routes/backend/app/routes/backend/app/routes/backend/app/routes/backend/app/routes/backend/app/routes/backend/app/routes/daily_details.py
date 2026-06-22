from fastapi import APIRouter, Depends
from ..database import supabase
from ..auth import get_current_user
from ..schemas import DailyDetail
from typing import List

router = APIRouter(prefix="/daily-details", tags=["daily-details"])

@router.get("/", response_model=List[DailyDetail])
async def get_daily_details(current_user = Depends(get_current_user)):
    query = supabase.table("daily_details").select("*")
    if current_user.role not in ["admin", "manager"]:
        query = query.eq("user_id", current_user.id)
    response = query.order("created_at", desc=True).execute()
    return response.data
