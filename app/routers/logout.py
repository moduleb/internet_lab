

from fastapi import APIRouter, Depends, Response

from app.container import auth_service

router = APIRouter()


# """LOGOUT"""
@router.post("/", summary="Logout")
async def get_all(current_username: str = Depends(auth_service.logout)):
    return Response(status_code=204)