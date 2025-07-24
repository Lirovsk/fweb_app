"""File to declare all the exceptions may used in the application"""

class NotFoundError(Exception):
    pass

class ValidationError(Exception):
    pass

class DatabaseError(Exception):
    pass

class CancelByUser(Exception):
    pass