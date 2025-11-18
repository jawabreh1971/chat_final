from fastapi import Header

async def get_role(x_role: str = Header(default="admin")):
    """
    Temporary role system:
    - If frontend sends nothing → role becomes "admin"
    - No authentication required
    """
    return x_role
