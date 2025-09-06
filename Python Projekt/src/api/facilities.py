import json
from fastapi import Body
from fastapi import APIRouter

from src.api.dependecies import DBDep
from src.schemas.facilities import FacilityAdd
from src.init import redis_connector


router = APIRouter(prefix="/facilities", tags=["Facilities"])


@router.get("")
async def get_facilities(db: DBDep):
    facilities_from_cashe = await redis_connector.get_value("facilities")
    print(f'facilities_from_cashe: {facilities_from_cashe}')
    if not facilities_from_cashe:
        facilities = await db.facilities.get_all()
        print(f'facilities: {facilities}')
        facilities_schemas: list[dict] = [facility.model_dump() for facility in facilities]
        print(f'facilities_schemas: {facilities_schemas}')
        facilities_json = json.dumps(facilities_schemas)
        print(f'facilities_json: {facilities_json}')
        await redis_connector.set_value("facilities", facilities_json, 100)

        return facilities
    else:
        facilities_dicts = json.loads(facilities_from_cashe)
        return facilities_dicts


@router.post("")
async def creat_facility(db: DBDep, facility_data: FacilityAdd = Body()):
    facility = await db.facilities.add(facility_data)
    await db.commit()
    return {"status": "OK", "data": facility}