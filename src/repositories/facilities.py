from sqlalchemy import insert, select, delete
from src.repositories.mappers.mappers import FacilitiesDataMapper
from src.repositories.base import BaseRepository
from src.schemas.facilities import RoomFacility
from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm


class FasilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    mapper = FacilitiesDataMapper


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    schema = RoomFacility

    async def set_room_facilities(self, room_id: int, facility_ids: list[int]):
        get_current_facilities_ids = select(self.model.facility_id).filter_by(room_id=room_id)
        res = await self.session.execute(get_current_facilities_ids)
        curr_facilities_ids = res.scalars().all()

        get_ids_to_delete = list(set(curr_facilities_ids) - set(facility_ids))
        get_ids_to_add = list(set(facility_ids) - set(curr_facilities_ids))

        if get_ids_to_delete:
            delete_stmt = (
                delete(self.model)
                .filter_by(room_id=room_id)
                .filter(self.model.facility_id.in_(get_ids_to_delete))
            )
            await self.session.execute(delete_stmt)

        if get_ids_to_add:
            add_stmt = insert(self.model).values(
                [{"room_id": room_id, "facility_id": facility_id} for facility_id in get_ids_to_add]
            )
            await self.session.execute(add_stmt)
