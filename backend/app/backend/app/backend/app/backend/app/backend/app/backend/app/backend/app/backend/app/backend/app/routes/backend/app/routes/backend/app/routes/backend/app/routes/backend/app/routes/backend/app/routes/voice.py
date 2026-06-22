from fastapi import APIRouter, File, UploadFile, Depends, BackgroundTasks, HTTPException
from ..database import supabase
from ..auth import get_current_user
from ..ai import extract_meeting_info
import openai
import os
import tempfile

router = APIRouter(prefix="/voice", tags=["voice"])

openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def transcribe_audio(file: UploadFile) -> str:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".m4a") as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name
    with open(tmp_path, "rb") as f:
        transcript = openai_client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
        )
    os.unlink(tmp_path)
    return transcript.text

def send_department_notifications(department: str, detail: dict, user_id: str):
    users = supabase.table("users")\
        .select("id")\
        .eq("department", department)\
        .filter("id", "neq", user_id)\
        .execute()
    for u in users.data:
        supabase.table("notifications").insert({
            "user_id": u["id"],
            "type": "daily_detail",
            "title": f"New Meeting Log: {detail['client_name']}",
            "message": f"Location: {detail['location']}\nWork: {detail['work_description']}\nDeadline: {detail.get('deadline', 'N/A')}",
            "data": {"detail_id": detail["id"]}
        }).execute()

@router.post("/process")
async def process_voice(
    background_tasks: BackgroundTasks,
    audio: UploadFile = File(...),
    lead_id: str = None,
    current_user = Depends(get_current_user)
):
    try:
        transcription = await transcribe_audio(audio)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {e}")

    extracted = extract_meeting_info(transcription)
    audio_url = None

    detail_data = {
        "user_id": current_user.id,
        "lead_id": lead_id,
        "location": extracted.get("location", ""),
        "work_description": extracted.get("work_description", ""),
        "client_name": extracted.get("client_name", ""),
        "client_contact": extracted.get("client_contact"),
        "deadline": extracted.get("deadline"),
        "next_meeting": extracted.get("next_meeting"),
        "department": extracted.get("department", "Sales"),
        "notes": extracted.get("notes"),
        "audio_url": audio_url,
        "transcription": transcription,
    }
    response = supabase.table("daily_details").insert(detail_data).execute()
    detail = response.data[0]

    background_tasks.add_task(send_department_notifications, detail["department"], detail, current_user.id)

    return {"detail": detail, "transcription": transcription}
  
