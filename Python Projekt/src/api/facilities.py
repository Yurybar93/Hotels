from fastapi import Body
from fastapi_cache.decorator import cache
from fastapi import APIRouter

from src.api.dependecies import DBDep
from src.schemas.facilities import FacilityAdd
from src.tasks.tasks import test_task


router = APIRouter(prefix="/facilities", tags=["Facilities"])


@router.get("")
@cache(expire=100)
async def get_facilities(db: DBDep):
    return await db.facilities.get_all()


@router.post("")
async def creat_facility(db: DBDep, facility_data: FacilityAdd = Body()):
    facility = await db.facilities.add(facility_data)

    test_task.delay()
    await db.commit()
    return {"status": "OK", "data": facility}
