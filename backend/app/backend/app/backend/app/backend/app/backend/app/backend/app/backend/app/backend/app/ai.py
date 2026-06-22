import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_meeting_info(transcription: str) -> dict:
    prompt = f"""
Extract the following fields from this meeting transcription:
- location
- work_description
- client_name
- client_contact (optional)
- deadline (YYYY-MM-DD)
- next_meeting (ISO datetime)
- department (choose from: Sales, Design, Production, Finance, HR, IT)

Transcription:
{transcription}

Return a JSON object with those keys.
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    content = response.choices[0].message.content
    try:
        return json.loads(content)
    except:
        return {}
