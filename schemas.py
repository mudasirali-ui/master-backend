from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
import uuid

class ContactForm(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    i_am: Optional[str] = None
    current_country: Optional[str] = None
    subject: Optional[str] = None
    message: Optional[str] = None

class ContactOut(BaseModel):
    id: uuid.UUID
    first_name: str
    last_name: str
    email: str
    phone: Optional[str]
    i_am: Optional[str]
    current_country: Optional[str]
    subject: Optional[str]
    message: Optional[str]
    resume_url: Optional[str]
    created_at: datetime
    is_read: bool
