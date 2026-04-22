from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from auth import hash_password, verify_password, create_token, get_current_user
from middleware.project import get_project_id
from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/api/auth", tags=["auth"])

class UserSignup(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

@router.post("/signup")
def signup(
    user: UserSignup,
    project_id: str = Depends(get_project_id),
    db=Depends(get_db)
):
    cur = db.cursor()
    cur.execute(
        "SELECT id FROM users WHERE email=%s AND project_id=%s",
        (user.email, project_id)
    )
    if cur.fetchone():
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = hash_password(user.password)
    cur.execute(
        """INSERT INTO users (project_id, name, email, password)
           VALUES (%s,%s,%s,%s)
           RETURNING id, name, email, created_at""",
        (project_id, user.name, user.email, hashed)
    )
    new_user = dict(cur.fetchone())
    db.commit()
    new_user["id"] = str(new_user["id"])
    token = create_token({"sub": new_user["id"], "project": project_id})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": new_user
    }

@router.post("/login")
def login(
    credentials: UserLogin,
    project_id: str = Depends(get_project_id),
    db=Depends(get_db)
):
    cur = db.cursor()
    cur.execute(
        "SELECT * FROM users WHERE email=%s AND project_id=%s",
        (credentials.email, project_id)
    )
    user = cur.fetchone()
    if not user or not verify_password(credentials.password, user["password"]):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    user = dict(user)
    user["id"] = str(user["id"])
    token = create_token({"sub": user["id"], "project": project_id})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "created_at": user["created_at"]
        }
    }

@router.get("/me")
def get_me(
    user_id: str = Depends(get_current_user),
    db=Depends(get_db)
):
    cur = db.cursor()
    cur.execute(
        "SELECT id, name, email, created_at FROM users WHERE id=%s",
        (user_id,)
    )
    user = cur.fetchone()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    r = dict(user)
    r["id"] = str(r["id"])
    return r