from src.schemas.facilities import FacilityAdd
from src.services.base import BaseService
from tasks.tasks import test_task


class FaciltyService(BaseService):
    async def creat_facility(self, data: FacilityAdd):
        facility = await self.db.facilities.add(data)
        await self.db.commit()

        test_task.delay()
        return facility
