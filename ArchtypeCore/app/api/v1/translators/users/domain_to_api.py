from app.api.v1.schemas.users import User as APIUser
from app.api.v1.schemas.users import UserList as APIUserList
from app.api.v1.schemas.users import UserStats as APIUserStats
from app.domain.schemas.users import User as DomainUser
from app.domain.schemas.users import UserList as DomainUserList
from app.domain.schemas.users import UserStats as DomainUserStats


def domain_to_api_user(domain: DomainUser) -> APIUser:

    """

    Convert Domain User to API User.

    """

    return APIUser.model_validate(domain)


def domain_to_api_user_stats(domain: DomainUserStats) -> APIUserStats:

    """

    Convert Domain UserStats to API UserStats.

    """

    return APIUserStats.model_validate(domain)


def domain_to_api_user_list(domain_users: DomainUserList) -> APIUserList:

    """

    Convert Domain UserList to API UserList.

    """

    api_users = [domain_to_api_user(u) for u in domain_users]


    return APIUserList(users=api_users)
