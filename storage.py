import os
import uuid
import httpx
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
BUCKET = "resumes"

async def upload_resume(file_bytes: bytes, filename: str, content_type: str) -> str:
    # Create unique filename so files don't overwrite each other
    ext = filename.split(".")[-1]
    unique_name = f"{uuid.uuid4()}.{ext}"
    
    url = f"{SUPABASE_URL}/storage/v1/object/{BUCKET}/{unique_name}"
    
    headers = {
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": content_type,
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, content=file_bytes, headers=headers)
    
    if response.status_code == 200:
        # Return the public URL of the uploaded file
        public_url = f"{SUPABASE_URL}/storage/v1/object/public/{BUCKET}/{unique_name}"
        return public_url
    else:
        raise Exception(f"Upload failed: {response.text}")
