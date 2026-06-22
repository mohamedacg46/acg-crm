from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import leads, activities, users, stats, voice, daily_details

app = FastAPI(title="ACG CRM API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(leads.router)
app.include_router(activities.router)
app.include_router(users.router)
app.include_router(stats.router)
app.include_router(voice.router)
app.include_router(daily_details.router)

@app.get("/")
async def root():
    return {"message": "ACG CRM API"}
  add main.py
