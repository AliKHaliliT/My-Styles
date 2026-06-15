class DomainException(Exception):

    """
    
    Base domain exception.
    
    """
    
    pass


class AuthenticationError(DomainException):

    """
    
    Raised when admin authentication fails.
    
    """
    
    pass


class EntityNotFoundError(DomainException):

    """
    
    Raised when a user or device does not exist.
    
    """
    
    pass
