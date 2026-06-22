from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..database import supabase
from ..schemas import Activity, ActivityCreate
from ..auth import get_current_user

router = APIRouter(prefix="/activities", tags=["activities"])

@router.get("/", response_model=List[Activity])
async def get_activities(current_user = Depends(get_current_user)):
    query = supabase.table("activities").select("*")
    if current_user.role not in ["admin", "manager"]:
        query = query.eq("user_id", current_user.id)
    response = query.order("date", desc=True).execute()
    return response.data

@router.post("/", response_model=Activity)
async def create_activity(activity: ActivityCreate, current_user = Depends(get_current_user)):
    data = activity.dict()
    data["user_id"] = current_user.id
    response = supabase.table("activities").insert(data).execute()
    return response.data[0]
