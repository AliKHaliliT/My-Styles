from typing import Any

from sqlalchemy import func, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domain.interfaces.repositories import IUserRepository
from app.domain.schemas.users import User as DomainUser
from app.domain.schemas.users import UserCreate as DomainUserCreate
from app.domain.schemas.users import UserUpdate as DomainUserUpdate
from app.models.user import User as DBUser
from app.repositories.translators.users import (db_to_domain_user,
                                                domain_to_db_user_create,
                                                domain_to_db_user_update)


class CRUDUser(IUserRepository):

    """

    SQLAlchemy implementation of the IUserRepository.


    Usage
    -----
    This class provides methods to perform CRUD operations on User entities
    using an asynchronous SQLAlchemy session.
    ```python
    from app.repositories.sqlalchemy import CRUDUser
    from app.domain.schemas.users import UserCreate, UserUpdate

    async with AsyncSession(engine) as session:
    
        user_repo = CRUDUser(session)

        # Create a new user
        new_user = await user_repo.add(UserCreate(username="john_doe", email="john@example.com"))
        # Get a user by ID
        user = await user_repo.get(new_user.id)
        # Update a user
        updated_user = await user_repo.update(user, UserUpdate(email="john.updated@example.com"))
        # Delete a user
        deleted_user = await user_repo.delete(updated_user.id)
    ```

    """

    def __init__(self, session: AsyncSession) -> None:

        """
        
        Initialize with AsyncSession.


        Parameters
        ----------
        session : AsyncSession
            The SQLAlchemy asynchronous session.

            
        Returns
        -------
        None.
        
        """

        if not isinstance(session, AsyncSession):
            raise TypeError(f"session must be an AsyncSession. Received: {session} with type {type(session)}")


        self.session = session
        self.model = DBUser


    async def get(self, id: Any) -> DomainUser | None:

        """
        
        Retrieve a User by ID. Eagerly loads devices.


        Parameters
        ----------
        id : Any
            The ID of the user.

            
        Returns
        -------
        DomainUser | None
            The mapped domain schema, or None if not found.
        
        """

        db_obj = await self.session.scalar(select(self.model).options(selectinload(self.model.devices)).where(self.model.id == id))
        return db_to_domain_user(db_obj) if db_obj else None


    async def get_by_username(self, username: str) -> DomainUser | None:

        """
        
        Retrieve a user by their username.


        Parameters
        ----------
        username : str
            The username to lookup.

            
        Returns
        -------
        DomainUser | None
            The mapped domain schema, or None if not found.
        
        """

        if not isinstance(username, str):
            raise TypeError(f"username must be a str. Received: {username} with type {type(username)}")


        db_obj = await self.session.scalar(select(self.model).options(selectinload(self.model.devices)).where(self.model.username == username))
        return db_to_domain_user(db_obj) if db_obj else None


    async def get_multi(self, skip: int = 0, limit: int = 100) -> list[DomainUser]:
        
        """
        
        Retrieve multiple users with pagination.


        Parameters
        ----------
        skip : int
            Number of records to skip.

        limit : int
            Maximum number of records to return.

            
        Returns
        -------
        list[DomainUser]
            A list of mapped domain schemas.
        
        """

        if not isinstance(skip, int):
            raise TypeError(f"skip must be an int. Received: {skip} with type {type(skip)}")
        if not isinstance(limit, int):
            raise TypeError(f"limit must be an int. Received: {limit} with type {type(limit)}")


        db_objs = await self.session.scalars(select(self.model).options(selectinload(self.model.devices)).offset(skip).limit(limit))
        return [db_to_domain_user(obj) for obj in db_objs]


    async def get_users_over_quota(self) -> list[DomainUser]:
        
        """
        
        Retrieve users who have exceeded their quota and are currently enabled.


        Parameters
        ----------
        None.

            
        Returns
        -------
        list[DomainUser]
            A list of mapped domain schemas.
        
        """

        db_objs = await self.session.scalars(
            select(self.model).options(selectinload(self.model.devices)).where(
                self.model.quota_bytes > 0,
                self.model.used_bytes >= self.model.quota_bytes,
                self.model.status == "enabled"
            )
        )
        return[db_to_domain_user(obj) for obj in db_objs]


    async def get_all_users_count(self) -> int:
        
        """
        
        Retrieve the total count of all users.


        Parameters
        ----------
        None.

            
        Returns
        -------
        int
            The total count of users.
        
        """

        count = await self.session.scalar(select(func.count(self.model.id)))
        return count or 0


    async def get_near_quota_users_count(self) -> int:
        
        """
        
        Retrieve the count of users who are near their quota limit (>= 80%).


        Parameters
        ----------
        None.

            
        Returns
        -------
        int
            The count of users near their quota.
        
        """

        count = await self.session.scalar(
            select(func.count(self.model.id)).where(
                self.model.quota_bytes > 0,
                self.model.used_bytes >= self.model.quota_bytes * 0.8,
                self.model.used_bytes < self.model.quota_bytes,
                self.model.status == "enabled"
            )
        )
        return count or 0


    async def add(self, entity_in: DomainUserCreate) -> DomainUser:

        """

        Add a new User record.


        Parameters
        ----------
        entity_in : DomainUserCreate
            The domain schema for creation.

            
        Returns
        -------
        DomainUser
            The newly created mapped domain schema.

        """

        if not isinstance(entity_in, DomainUserCreate):
            raise TypeError(f"entity_in must be a DomainUserCreate. Received: {entity_in} with type {type(entity_in)}")


        db_obj = domain_to_db_user_create(domain_obj=entity_in)
        
        self.session.add(db_obj)
        await self.session.flush()
        await self.session.refresh(db_obj, attribute_names=['devices'])

        return db_to_domain_user(db_obj)


    async def update(self, db_obj: DomainUser, obj_in: DomainUserUpdate) -> DomainUser:

        """

        Update a User record.


        Parameters
        ----------
        db_obj : DomainUser
            The existing domain representation.

        obj_in : DomainUserUpdate
            The domain schema containing updates to apply.

            
        Returns
        -------
        DomainUser
            The updated mapped domain schema.

        """

        if not isinstance(db_obj, DomainUser):
            raise TypeError(f"db_obj must be a DomainUser. Received: {db_obj} with type {type(db_obj)}")
        if not isinstance(obj_in, DomainUserUpdate):
            raise TypeError(f"obj_in must be a DomainUserUpdate. Received: {obj_in} with type {type(obj_in)}")


        db_model = await self.session.scalar(select(self.model).options(selectinload(self.model.devices)).where(self.model.id == db_obj.id))
        if not db_model:
            raise NoResultFound(f"User with id {db_obj.id} not found")

        update_data = domain_to_db_user_update(domain_obj=obj_in)

        for field, value in update_data.items():
            if hasattr(db_model, field):
                setattr(db_model, field, value)

        self.session.add(db_model)
        await self.session.flush()
        await self.session.refresh(db_model, attribute_names=['devices'])

        return db_to_domain_user(db_model)


    async def delete(self, id: int) -> DomainUser:

        """

        Delete a User by ID.


        Parameters
        ----------
        id : int
            The ID of the user.

            
        Returns
        -------
        DomainUser
            The deleted mapped domain schema.

        """

        if not isinstance(id, int):
            raise TypeError(f"id must be an int. Received: {id} with type {type(id)}")


        db_model = await self.session.scalar(select(self.model).options(selectinload(self.model.devices)).where(self.model.id == id))
        if db_model is None:
            raise NoResultFound(f"User with id {id} not found")

        domain_obj = db_to_domain_user(db_model)
        await self.session.delete(db_model)
        await self.session.flush()

        return domain_obj
