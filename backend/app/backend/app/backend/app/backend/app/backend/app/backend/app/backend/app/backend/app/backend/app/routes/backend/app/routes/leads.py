from fastapi import APIRouter, Depends, HTTPException
from typing import Optional, List
from ..database import supabase
from ..schemas import Lead, LeadCreate, LeadUpdate
from ..auth import get_current_user
from datetime import datetime

router = APIRouter(prefix="/leads", tags=["leads"])

@router.get("/", response_model=List[Lead])
async def get_leads(
    status: Optional[str] = None,
    assigned_to: Optional[str] = None,
    search: Optional[str] = None,
    current_user = Depends(get_current_user)
):
    query = supabase.table("leads").select("*").eq("is_deleted", False)
    if current_user.role not in ["admin", "manager"]:
        query = query.eq("assigned_to", current_user.id)
    if status:
        query = query.eq("status", status)
    if assigned_to:
        query = query.eq("assigned_to", assigned_to)
    if search:
        query = query.or_(f"company_name.ilike.%{search}%,contact_person.ilike.%{search}%")
    response = query.order("created_at", desc=True).execute()
    return response.data

@router.get("/{lead_id}", response_model=Lead)
async def get_lead(lead_id: str, current_user = Depends(get_current_user)):
    query = supabase.table("leads").select("*").eq("id", lead_id).eq("is_deleted", False)
    response = query.execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Lead not found")
    return response.data[0]

@router.post("/", response_model=Lead)
async def create_lead(lead: LeadCreate, current_user = Depends(get_current_user)):
    year = datetime.now().year
    count_res = supabase.table("leads").select("id", count="exact").execute()
    count = count_res.count or 0
    lead_id = f"ACG-{year}-{count+1:04d}"
    data = lead.dict()
    data["lead_id"] = lead_id
    data["assigned_to"] = data.get("assigned_to") or current_user.id
    data["is_deleted"] = False
    response = supabase.table("leads").insert(data).execute()
    return response.data[0]

@router.put("/{lead_id}", response_model=Lead)
async def update_lead(lead_id: str, lead_update: LeadUpdate, current_user = Depends(get_current_user)):
    data = lead_update.dict(exclude_unset=True)
    data["updated_at"] = datetime.now().isoformat()
    response = supabase.table("leads").update(data).eq("id", lead_id).eq("is_deleted", False).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Lead not found")
    return response.data[0]

@router.delete("/{lead_id}")
async def delete_lead(lead_id: str, current_user = Depends(get_current_user)):
    response = supabase.table("leads").update({"is_deleted": True, "updated_at": datetime.now().isoformat()}).eq("id", lead_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Lead not found")
    return {"message": "Lead deleted"}
