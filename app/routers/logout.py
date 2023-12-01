

from fastapi import APIRouter, Depends


from app.services.auth_service import AuthService

router = APIRouter()

# LOGOUT
@router.post("/logout", status_code=204, summary="Logout")
async def logout(username: str = Depends(AuthService.logout)):
    pass