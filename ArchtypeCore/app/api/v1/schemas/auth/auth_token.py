from pydantic import BaseModel, ConfigDict


class AuthTokenBase(BaseModel):

    """
    
    Base API schema shared across token variants.
    
    """
    
    token_type: str
    access_token: str
    expires_in: int


class AuthToken(AuthTokenBase):

    """

    API schema representing an access token.

    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "token_type": "bearer",
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsInJvbGU...",
                "expires_in": 1800
            }
        }
    )
