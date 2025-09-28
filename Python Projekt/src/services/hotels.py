from datetime import date
from src.schemas.hotels import Hotel, HotelAdd, HotelPATCH
from src.exceptions import (
    HotelNotFoundException,
    ObjectNotFoundException,
    UncorrectDataException,
    UncorrectHotelDataException,
    check_date_from_bigger_than_date_to,
)
from src.services.base import BaseService


class HotelService(BaseService):
    async def get_hotels(
        self,
        pagination,
        title: str | None,
        location: str | None,
        date_from: date,
        date_to: date,
    ):
        per_page = pagination.per_page or 5
        check_date_from_bigger_than_date_to(date_from, date_to)
        return await self.db.hotels.get_filtered_by_time(
            date_from=date_from,
            date_to=date_to,
            title=title,
            location=location,
            limit=per_page,
            offset=(pagination.page - 1) * per_page,
        )

    async def get_hotel(self, hotel_id: int):
        return await self.db.hotels.get_one(id=hotel_id)

    async def create_hotel(self, hotel_data: HotelAdd):
        hotel = await self.db.hotels.add(hotel_data)
        await self.db.commit()
        return hotel

    async def update_hotel(self, hotel_id: int, hotel_data: HotelAdd):
        await self.db.hotels.edit(hotel_data, id=hotel_id)
        await self.db.commit()

    async def patch_hotel(self, hotel_id: int, hotel_data: HotelPATCH):
        await self.db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
        await self.db.commit()

    async def delete_hotel(self, hotel_id: int):
        await self.db.hotels.delete(id=hotel_id)
        await self.db.commit()

    async def get_hotel_with_check(self, hotel_id: int) -> Hotel:
        try:
            return await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundException
        except UncorrectDataException:
            raise UncorrectHotelDataException
