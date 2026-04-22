from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from typing import Optional

try:
    from ..database import get_db
    from ..storage import upload_resume
    from ..middleware.project import get_project_id
except ImportError:
    # Allows running from inside `backend` with `uvicorn main:app`.
    from database import get_db
    from storage import upload_resume
    from middleware.project import get_project_id

router = APIRouter(prefix="/api/contact", tags=["contact"])

ALLOWED_TYPES = ["application/pdf", "application/msword",
                 "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]
MAX_SIZE = 5 * 1024 * 1024  # 5MB

@router.post("/submit")
async def submit_contact(
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    phone: Optional[str] = Form(None),
    i_am: Optional[str] = Form(None),
    current_country: Optional[str] = Form(None),
    subject: Optional[str] = Form(None),
    message: Optional[str] = Form(None),
    resume: Optional[UploadFile] = File(None),
    project_id: str = Depends(get_project_id),
    db=Depends(get_db)
):
    resume_url = None

    # Handle file upload if provided
    if resume and resume.filename:
        # Check file type
        if resume.content_type not in ALLOWED_TYPES:
            raise HTTPException(
                status_code=400,
                detail="Only PDF, DOC, DOCX files allowed"
            )
        
        # Read file and check size
        file_bytes = await resume.read()
        if len(file_bytes) > MAX_SIZE:
            raise HTTPException(
                status_code=400,
                detail="File too large. Max 5MB allowed"
            )
        
        # Upload to Supabase Storage
        try:
            resume_url = await upload_resume(file_bytes, resume.filename, resume.content_type)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")

    # Save to database
    try:
        cur = db.cursor()
        cur.execute(
            """
            INSERT INTO contacts 
            (project_id, first_name, last_name, email, phone, i_am, current_country, subject, message, resume_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id, created_at
            """,
            (project_id, first_name, last_name, email, phone, i_am,
             current_country, subject, message, resume_url)
        )
        saved = cur.fetchone()
        db.commit()

        return {
            "success": True,
            "message": "Thank you! We will be in touch soon.",
            "id": str(saved["id"])
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to save enquiry")


@router.get("/all")
def get_all_contacts(project_id: str = Depends(get_project_id), db=Depends(get_db)):
    cur = db.cursor()
    cur.execute(
        "SELECT * FROM contacts WHERE project_id=%s ORDER BY created_at DESC",
        (project_id,)
    )
    rows = cur.fetchall()
    # Convert UUID to string for JSON
    result = []
    for row in rows:
        r = dict(row)
        r["id"] = str(r["id"])
        result.append(r)
    return result
