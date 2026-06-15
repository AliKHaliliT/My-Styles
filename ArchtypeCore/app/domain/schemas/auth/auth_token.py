from pydantic import BaseModel


class AuthTokenBase(BaseModel):

    """
    
    Base Domain schema shared across token variants.
    
    """
    
    token_type: str
    access_token: str
    expires_in: int


class AuthToken(AuthTokenBase):

    """

    Domain schema representing an access token.

    """

    pass
