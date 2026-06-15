from app.api.v1.schemas.auth import AuthToken as APIAuthToken
from app.domain.schemas.auth import AuthToken as DomainAuthToken


def domain_to_api_auth_token(domain: DomainAuthToken) -> APIAuthToken:

    """

    Convert Domain AuthToken to API AuthToken.

    """

    return APIAuthToken.model_validate(domain)
