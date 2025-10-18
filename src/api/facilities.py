from fastapi import Body
from fastapi_cache.decorator import cache
from fastapi import APIRouter

from src.exceptions import FacilityAlreadyExistsHTTPException, ObjectAlreadyExistsException
from src.api.dependecies import DBDep
from src.schemas.facilities import FacilityAdd
from src.services.facilities import FaciltyService


router = APIRouter(prefix="/facilities", tags=["Facilities"])


@router.get("")
@cache(expire=100)
async def get_facilities(db: DBDep):
    return await db.facilities.get_all()


@router.post("")
async def creat_facility(db: DBDep, facility_data: FacilityAdd = Body()):
    try:
        facility = await FaciltyService(db).creat_facility(facility_data)
    except ObjectAlreadyExistsException:
        raise FacilityAlreadyExistsHTTPException
    return {"status": "OK", "data": facility}
