from datetime import date
from fastapi import HTTPException


class MyAppException(Exception):
    detail = "Unexpected error"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(MyAppException):
    detail = "Object not found"


class RoomNotFoundException(ObjectNotFoundException):
    detail = "Room not found"


class HotelNotFoundException(ObjectNotFoundException):
    detail = "Hotel not found"


class UserNotFoundException(ObjectNotFoundException):
    detail = "User not found"


class UncorrectPasswordException(MyAppException):
    detail = "Uncorrect password"


class AllRoomsBookedException(MyAppException):
    detail = "All rooms are booked"


class UncorrectDataException(MyAppException):
    detail = "Uncorrect data"


class UncorrectHotelDataException(UncorrectDataException):
    detail = "Uncorrect hotel data"


class UncorrectRoomDataException(UncorrectDataException):
    detail = "Uncorrect room data"


class ObjectAlreadyExistsException(MyAppException):
    detail = "Object with this identifier already exists"


class UserAlreadyExistsException(ObjectAlreadyExistsException):
    detail = "User with this identifier already exists"


class HotelAlreadyExistsException(ObjectAlreadyExistsException):
    detail = "Hotel already exists"


class ForeinKeyViolationException(MyAppException):
    detail = "Foreign key violation error"


class ForeinKeyRoomViolationException(ForeinKeyViolationException):
    detail = "Foreign key violation error"


def check_date_from_bigger_than_date_to(date_from: date, date_to: date):
    if date_from >= date_to:
        raise HTTPException(status_code=400, detail="date_from must be earlier than date_to")


class MyAppHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class HotelNotFoundHTTPException(MyAppHTTPException):
    status_code = 404
    detail = "Hotel not found"


class RoomNotFoundHTTPException(MyAppHTTPException):
    status_code = 404
    detail = "Room not found"


class UncorrectHotelIDHTTPException(MyAppHTTPException):
    status_code = 400
    detail = "Uncorrect hotel ID"


class UncorrectRoomIDHTTPException(MyAppHTTPException):
    status_code = 400
    detail = "Uncorrect room ID"


class ForeignKeyViolationErrorHTTPException(MyAppHTTPException):
    status_code = 400
    detail = "Blocked: this object is used elsewhere."


class UserAlreadyExistsHTTPException(MyAppHTTPException):
    status_code = 409
    detail = "User with this email already exists"


class HotelAlreadyExistsHTTPException(MyAppHTTPException):
    status_code = 409
    detail = "Hotel with this title and location already exists"


class RoomAlreadyExistsHTTPException(MyAppHTTPException):
    status_code = 409
    detail = "Room with this title, description and price already exists in this hotel"


class FacilityAlreadyExistsHTTPException(MyAppHTTPException):
    status_code = 409
    detail = "Facility with this title already exists"


class UserNotFoundHTTPException(MyAppHTTPException):
    status_code = 404
    detail = "User not found"


class UncorrectPasswordHTTPException(MyAppHTTPException):
    status_code = 401
    detail = "Uncorrect password"


class InvalidTokenHTTPException(MyAppHTTPException):
    status_code = 401
    detail = "Invalid token"


class NoAccessTokenHTTPException(MyAppHTTPException):
    status_code = 401
    detail = "No access token"


class AllRoomsBookedHTTPException(MyAppHTTPException):
    status_code = 409
    detail = "All rooms are booked"


class FacilitisNotExistsHTTPException(MyAppHTTPException):
    status_code = 400
    detail = "One or more facilities do not exist"
