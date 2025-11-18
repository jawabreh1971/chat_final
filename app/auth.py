
import os
from typing import Optional
from fastapi import Header

ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "CHANGE_ME_ADMIN_TOKEN")

async def get_role(x_admin_token: Optional[str] = Header(default=None)) -> str:
    """Simple role resolution based on X-Admin-Token header."""
    if x_admin_token and x_admin_token == ADMIN_TOKEN:
        return "admin"
    return "user"
