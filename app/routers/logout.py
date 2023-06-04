

from fastapi import APIRouter, Depends, Response, Request

from app.container import auth_service
from app.limiter import limiter

router = APIRouter()

# """LOGOUT"""
@router.post("/", summary="Logout")
@limiter.limit("5/minute")
async def get_all(request: Request,
                  current_username: str = Depends(auth_service.logout)):
    return Response(status_code=204)