from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.access_request import AccessRequestIn, AccessRequestOut, AccessRequestStatusUpdate
from app.services import access as svc
from app.auth import require_admin

router = APIRouter()

@router.post("/", response_model=AccessRequestOut, status_code=201)
async def submit_access_request(data: AccessRequestIn, db: AsyncSession = Depends(get_db)):
    return await svc.create_access_request(data, db)

@router.get("/", response_model=list[AccessRequestOut], dependencies=[Depends(require_admin)])
async def list_requests(db: AsyncSession = Depends(get_db)):
    return await svc.list_access_requests(db)

@router.patch("/{id}/status", response_model=AccessRequestStatusUpdate, dependencies=[Depends(require_admin)])
async def update_status(
    id: int,
    status: str = Query(...),
    db: AsyncSession = Depends(get_db)
):
    if status not in ("pending", "approved", "rejected"):
        raise HTTPException(status_code=400, detail="Invalid status value")
    return await svc.update_access_request_status(id, status, db)