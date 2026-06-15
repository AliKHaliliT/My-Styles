from typing import Any

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.interfaces.repositories import IAdminRepository
from app.domain.interfaces.security import IAuthManager
from app.domain.schemas.admins import AdminCreate as DomainAdminCreate
from app.domain.schemas.admins import AdminInDB as DomainAdminInDB
from app.domain.schemas.admins import AdminUpdate as DomainAdminUpdate
from app.models.admin import Admin as DBAdmin
from app.repositories.translators.admins import (db_to_domain_admin_in_db,
                                                 domain_to_db_admin_create,
                                                 domain_to_db_admin_update)


class CRUDAdmin(IAdminRepository):

    """

    SQLAlchemy implementation of the IAdminRepository.


    Usage
    -----
    This class provides methods to perform CRUD operations on Admin entities
    using an asynchronous SQLAlchemy session. It also integrates with an
    authentication manager for password hashing.
    ```python
    from app.repositories.sqlalchemy import CRUDAdmin
    from app.domain.schemas.admins import AdminCreate, AdminUpdate

    async with AsyncSession(engine) as session:
    
        auth_manager = YourAuthManager()
        admin_repo = CRUDAdmin(session, auth_manager)

        # Create a new admin
        new_admin = await admin_repo.add(AdminCreate(username="admin1", password="secret", role="admin"))
        # Get an admin by ID
        admin = await admin_repo.get(new_admin.id)
        # Update an admin
        updated_admin = await admin_repo.update(admin, AdminUpdate(role="superadmin"))
        # Delete an admin
        deleted_admin = await admin_repo.delete(updated_admin.id)
    ```

    """

    def __init__(self, session: AsyncSession, auth_manager: IAuthManager) -> None:

        """
        
        Initialize with AsyncSession and AuthManager.


        Parameters
        ----------
        session : AsyncSession
            The SQLAlchemy asynchronous session.

        auth_manager : IAuthManager
            The authentication manager.

            
        Returns
        -------
        None.
        
        """

        if not isinstance(session, AsyncSession):
            raise TypeError(f"session must be an AsyncSession. Received: {session} with type {type(session)}")
        if not isinstance(auth_manager, IAuthManager):
            raise TypeError(f"auth_manager must implement IAuthManager. Received: {auth_manager} with type {type(auth_manager)}")


        self.session = session
        self.model = DBAdmin
        self.auth_manager = auth_manager


    async def get(self, id: Any) -> DomainAdminInDB | None:

        """
        
        Retrieve an Admin by ID.


        Parameters
        ----------
        id : Any
            The ID of the admin.

            
        Returns
        -------
        DomainAdminInDB | None
            The mapped domain schema, or None if not found.
        
        """

        db_obj = await self.session.scalar(select(self.model).where(self.model.id == id))
        return db_to_domain_admin_in_db(db_obj) if db_obj else None


    async def get_by_username(self, username: str) -> DomainAdminInDB | None:

        """
        
        Retrieve an Admin by username.


        Parameters
        ----------
        username : str
            The username of the admin.

            
        Returns
        -------
        DomainAdminInDB | None
            The mapped domain schema, or None if not found.
        
        """

        if not isinstance(username, str):
            raise TypeError(f"username must be a str. Received: {username} with type {type(username)}")


        db_obj = await self.session.scalar(select(self.model).where(self.model.username == username))
        return db_to_domain_admin_in_db(db_obj) if db_obj else None


    async def add(self, entity_in: DomainAdminCreate) -> DomainAdminInDB:

        """

        Add a new Admin record.


        Parameters
        ----------
        entity_in : DomainAdminCreate
            The domain schema for creation.

            
        Returns
        -------
        DomainAdminInDB
            The newly created mapped domain schema.

        """

        if not isinstance(entity_in, DomainAdminCreate):
            raise TypeError(f"entity_in must be an DomainAdminCreate. Received: {entity_in} with type {type(entity_in)}")


        hashed_password = self.auth_manager.get_password_hash(entity_in.password)
        db_obj = domain_to_db_admin_create(domain_obj=entity_in, hashed_password=hashed_password)

        self.session.add(db_obj)
        await self.session.flush()
        await self.session.refresh(db_obj)

        return db_to_domain_admin_in_db(db_obj)
    

    async def update(self, db_obj: DomainAdminInDB, obj_in: DomainAdminUpdate) -> DomainAdminInDB:

        """

        Update an Admin record.


        Parameters
        ----------
        db_obj : DomainAdminInDB
            The existing domain representation.

        obj_in : DomainAdminUpdate
            The domain schema containing updates to apply.

            
        Returns
        -------
        DomainAdminInDB
            The updated mapped domain schema.

        """

        if not isinstance(db_obj, DomainAdminInDB):
            raise TypeError(f"db_obj must be an DomainAdminInDB. Received: {db_obj} with type {type(db_obj)}")
        if not isinstance(obj_in, DomainAdminUpdate):
            raise TypeError(f"obj_in must be a DomainAdminUpdate. Received: {obj_in} with type {type(obj_in)}")


        db_model = await self.session.scalar(select(self.model).where(self.model.id == db_obj.id))
        if not db_model:
            raise NoResultFound(f"Admin with id {db_obj.id} not found")

        hashed_pw = None
        if obj_in.password is not None:
            hashed_pw = self.auth_manager.get_password_hash(obj_in.password)
            
        update_data = domain_to_db_admin_update(domain_obj=obj_in, hashed_password=hashed_pw)

        for field, value in update_data.items():
            if hasattr(db_model, field):
                setattr(db_model, field, value)

        self.session.add(db_model)
        await self.session.flush()
        await self.session.refresh(db_model)

        return db_to_domain_admin_in_db(db_model)


    async def delete(self, id: int) -> DomainAdminInDB:

        """

        Delete an Admin by ID.


        Parameters
        ----------
        id : int
            The ID of the admin.

            
        Returns
        -------
        DomainAdminInDB
            The deleted mapped domain schema.

        """

        if not isinstance(id, int):
            raise TypeError(f"id must be an int. Received: {id} with type {type(id)}")


        db_model = await self.session.scalar(select(self.model).where(self.model.id == id))
        if db_model is None:
            raise NoResultFound(f"Admin with id {id} not found")

        domain_obj = db_to_domain_admin_in_db(db_model)
        await self.session.delete(db_model)
        await self.session.flush()

        return domain_obj
