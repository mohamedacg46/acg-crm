from fastapi import APIRouter, Depends
from ..database import supabase
from ..auth import get_current_user
from datetime import date

router = APIRouter(prefix="/stats", tags=["stats"])

@router.get("/")
async def get_stats(current_user = Depends(get_current_user)):
    query = supabase.table("leads").select("*").eq("is_deleted", False)
    if current_user.role not in ["admin", "manager"]:
        query = query.eq("assigned_to", current_user.id)
    leads = query.execute().data

    total = len(leads)
    won = len([l for l in leads if l["status"] == "Won"])
    lost = len([l for l in leads if l["status"] == "Lost"])
    revenue = sum(l["budget"] for l in leads if l["status"] == "Won")
    pipeline = sum(l["budget"] for l in leads if l["status"] in ["Qualified", "Proposal", "Negotiation"])

    today = date.today().isoformat()
    overdue = len([l for l in leads if l["next_followup"] and l["next_followup"] < today and l["status"] not in ["Won","Lost"]])

    return {
        "total": total,
        "won": won,
        "lost": lost,
        "revenue": revenue,
        "pipeline_value": pipeline,
        "win_rate": round(won/(won+lost)*100,1) if (won+lost)>0 else 0,
        "overdue_followups": overdue,
    }
