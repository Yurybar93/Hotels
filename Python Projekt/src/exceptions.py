


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


class DateFromBiggerThanDateToException(MyAppException):
    detail = "date_from must be earlier than date_to"


