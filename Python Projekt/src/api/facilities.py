from fastapi import Body, HTTPException, Query
from fastapi import APIRouter

from src.api.dependecies import DBDep
from src.schemas.facilities import FacilityAdd


router = APIRouter(prefix="/facilities", tags=["Facilities"])


@router.get("")
async def get_facilities(db: DBDep):
    return await db.facilities.get_all()


@router.post("")
async def creat_facility(
    db: DBDep,
    facility_data: FacilityAdd = Body()
    
):
    facility = await db.facilities.add(facility_data)
    await db.commit()
    return {"status": "OK", "data": facility}