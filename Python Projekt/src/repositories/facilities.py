from src.repositories.base import BaseRepository
from src.schemas.facilities import Facility
from src.models.facilities import FacilitiesOrm

class FasilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = Facility