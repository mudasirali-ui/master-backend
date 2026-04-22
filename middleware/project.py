import os
from fastapi import Request, HTTPException


def _default_project_id() -> str:
    explicit_project_id = os.getenv("PROJECT_ID", "").strip()
    if explicit_project_id:
        return explicit_project_id

    supabase_url = os.getenv("SUPABASE_URL", "").strip()
    if not supabase_url:
        return ""

    # Example: https://abcdefgh.supabase.co -> abcdefgh
    try:
        host = supabase_url.split("://", 1)[-1].split("/", 1)[0]
        return host.split(".", 1)[0].strip()
    except Exception:
        return ""


def get_project_id(request: Request) -> str:
    project_id = (request.headers.get("x-project-id") or "").strip()
    if project_id:
        return project_id

    # Resolve from current environment each request because env loading may
    # occur after module imports during app startup.
    default_project_id = _default_project_id()
    if default_project_id:
        return default_project_id

    if not project_id:
        raise HTTPException(
            status_code=400,
            detail="Missing x-project-id header and no default PROJECT_ID configured on server."
        )
    return project_id