


from datetime import date
from fastapi import HTTPException


class MyAppException(Exception):
    detail = "Unexpected error"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(MyAppException):
    detail = "Object not found"


class AllRoomsBookedException(MyAppException):
    detail = "All rooms are booked"


class UncorrectDataException(MyAppException):
    detail = "Uncorrect data"


class DataBaseException(MyAppException):
    detail = "Database error"


class ObjectAlreadyExistsException(MyAppException):
    detail = "Object with this identifier already exists"


class ForeinKeyViolationException(MyAppException):
    detail = "Foreign key violation error"


def check_date_from_bigger_than_date_to(date_from: date, date_to: date):
    if date_from >= date_to:
        raise HTTPException(status_code=400, detail="date_from must be earlier than date_to")
    

class MyAppHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)
    

class HotelNotFoundException(MyAppHTTPException):
    status_code = 404
    detail = "Hotel not found"


class RoomNotFoundException(MyAppHTTPException):
    status_code = 404
    detail = "Room not found"


class UncorrectHotelIDException(MyAppHTTPException):
    status_code = 400
    detail = "Uncorrect hotel ID"


class ForeignKeyViolationErrorHTTPException(MyAppHTTPException):
    status_code = 400
    detail = "Blocked: this object is used elsewhere."


