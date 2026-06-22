from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    role: str = "bdm"
    department: Optional[str] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: str
    created_at: datetime

class LeadBase(BaseModel):
    company_name: str
    contact_person: str
    phone: str
    email: Optional[str] = None
    area: str
    category: str
    budget: float = 0
    priority: str = "Medium"
    status: str = "New"
    source: str = "Other"
    date_added: date
    next_followup: Optional[date] = None
    notes: Optional[str] = None
    assigned_to: Optional[str] = None

class LeadCreate(LeadBase):
    pass

class LeadUpdate(BaseModel):
    company_name: Optional[str] = None
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    area: Optional[str] = None
    category: Optional[str] = None
    budget: Optional[float] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    source: Optional[str] = None
    date_added: Optional[date] = None
    next_followup: Optional[date] = None
    notes: Optional[str] = None
    assigned_to: Optional[str] = None

class Lead(LeadBase):
    id: str
    lead_id: str
    is_deleted: bool
    created_at: datetime
    updated_at: datetime

class ActivityBase(BaseModel):
    date: date
    company: str
    contact: Optional[str] = None
    purpose: str
    outcome: str
    notes: Optional[str] = None
    lead_id: Optional[str] = None

class ActivityCreate(ActivityBase):
    user_id: str

class Activity(ActivityBase):
    id: str
    user_id: str
    created_at: datetime

class DailyDetailBase(BaseModel):
    location: str
    work_description: str
    client_name: str
    client_contact: Optional[str] = None
    deadline: Optional[date] = None
    next_meeting: Optional[datetime] = None
    department: str
    notes: Optional[str] = None
    audio_url: Optional[str] = None
    transcription: Optional[str] = None

class DailyDetailCreate(DailyDetailBase):
    user_id: str
    lead_id: Optional[str] = None

class DailyDetail(DailyDetailBase):
    id: str
    user_id: str
    lead_id: Optional[str] = None
    created_at: datetime
